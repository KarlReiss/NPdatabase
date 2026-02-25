package cn.npdb.controller;

import cn.npdb.common.ApiCode;
import cn.npdb.common.ApiResponse;
import cn.npdb.common.PageResponse;
import cn.npdb.dto.BioactivityTargetSummary;
import cn.npdb.entity.BioResource;
import cn.npdb.entity.BioResourceNaturalProduct;
import cn.npdb.entity.Bioactivity;
import cn.npdb.entity.NaturalProduct;
import cn.npdb.entity.NaturalProductDetailView;
import cn.npdb.entity.Target;
import cn.npdb.mapper.BioactivityMapper;
import cn.npdb.service.BioResourceNaturalProductService;
import cn.npdb.service.BioResourceService;
import cn.npdb.service.BioactivityService;
import cn.npdb.service.NaturalProductService;
import cn.npdb.service.TargetService;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import org.springframework.beans.BeanUtils;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.math.BigDecimal;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/natural-products")
public class NaturalProductController {
    private static final long MAX_PAGE_SIZE = 200;
    private static final Pattern SAFE_LITERAL = Pattern.compile("^[A-Za-z0-9_\\- .]+$");

    private final NaturalProductService naturalProductService;
    private final BioactivityService bioactivityService;
    private final TargetService targetService;
    private final BioResourceService bioResourceService;
    private final BioResourceNaturalProductService bioResourceNaturalProductService;
    private final BioactivityMapper bioactivityMapper;

    public NaturalProductController(NaturalProductService naturalProductService,
                                    BioactivityService bioactivityService,
                                    TargetService targetService,
                                    BioResourceService bioResourceService,
                                    BioResourceNaturalProductService bioResourceNaturalProductService,
                                    BioactivityMapper bioactivityMapper) {
        this.naturalProductService = naturalProductService;
        this.bioactivityService = bioactivityService;
        this.targetService = targetService;
        this.bioResourceService = bioResourceService;
        this.bioResourceNaturalProductService = bioResourceNaturalProductService;
        this.bioactivityMapper = bioactivityMapper;
    }

    @GetMapping
    public ApiResponse<PageResponse<NaturalProductDetailView>> list(
            @RequestParam(defaultValue = "1") long page,
            @RequestParam(defaultValue = "20") long pageSize,
            @RequestParam(required = false) String q,
            @RequestParam(required = false) BigDecimal mwMin,
            @RequestParam(required = false) BigDecimal mwMax,
            @RequestParam(required = false) BigDecimal xlogpMin,
            @RequestParam(required = false) BigDecimal xlogpMax,
            @RequestParam(required = false) BigDecimal psaMin,
            @RequestParam(required = false) BigDecimal psaMax,
            @RequestParam(required = false) String activityType,
            @RequestParam(required = false) BigDecimal activityMaxNm,
            @RequestParam(required = false) String targetType
    ) {
        long safePage = page < 1 ? 1 : page;
        long safePageSize = pageSize < 1 ? 20 : Math.min(pageSize, MAX_PAGE_SIZE);

        QueryWrapper<NaturalProduct> wrapper = new QueryWrapper<>();
        wrapper.select(
                "id",
                "np_id",
                "pref_name",
                "iupac_name",
                "pubchem_id",
                "molecular_weight",
                "xlogp",
                "psa",
                "formula",
                "num_of_activity",
                "num_of_target",
                "num_of_organism"
        );

        if (StringUtils.hasText(q)) {
            wrapper.and(w -> w.like("pref_name", q)
                    .or().like("np_id", q)
                    .or().like("iupac_name", q));
        }
        if (mwMin != null) {
            wrapper.ge("molecular_weight", mwMin);
        }
        if (mwMax != null) {
            wrapper.le("molecular_weight", mwMax);
        }
        if (xlogpMin != null) {
            wrapper.ge("xlogp", xlogpMin);
        }
        if (xlogpMax != null) {
            wrapper.le("xlogp", xlogpMax);
        }
        if (psaMin != null) {
            wrapper.ge("psa", psaMin);
        }
        if (psaMax != null) {
            wrapper.le("psa", psaMax);
        }

        if (StringUtils.hasText(activityType) || activityMaxNm != null || StringUtils.hasText(targetType)) {
            StringBuilder sub = new StringBuilder();
            sub.append("select distinct b.natural_product_id from bioactivity b left join targets t on b.target_id = t.id where 1=1");

            if (StringUtils.hasText(activityType)) {
                String safe = requireSafeLiteral(activityType, "activityType");
                sub.append(" and b.activity_type = '").append(safe).append("'");
            }
            if (activityMaxNm != null) {
                sub.append(" and b.activity_value_std <= ").append(activityMaxNm);
            }
            if (StringUtils.hasText(targetType)) {
                String safe = requireSafeLiteral(targetType, "targetType");
                sub.append(" and t.target_type = '").append(safe).append("'");
            }

            wrapper.inSql("id", sub.toString());
        }
        wrapper.orderByDesc("id");

        Page<NaturalProduct> mpPage = new Page<>(safePage, safePageSize, true);
        Page<NaturalProduct> result = naturalProductService.page(mpPage, wrapper);

        List<NaturalProduct> records = result.getRecords();
        if (records.isEmpty()) {
            return ApiResponse.ok(new PageResponse<>(Collections.emptyList(), result.getCurrent(), result.getSize(), result.getTotal()));
        }

        List<Long> ids = records.stream().map(NaturalProduct::getId).collect(Collectors.toList());

        QueryWrapper<Bioactivity> aggWrapper = new QueryWrapper<>();
        aggWrapper.select(
                "natural_product_id as naturalProductId",
                "COUNT(*) as bioactivityCount",
                "COUNT(DISTINCT target_id) as targetCount",
                "MIN(COALESCE(activity_value_std, activity_value)) as bestActivityValue"
        );
        aggWrapper.in("natural_product_id", ids);
        aggWrapper.groupBy("natural_product_id");

        List<java.util.Map<String, Object>> aggRows = bioactivityService.listMaps(aggWrapper);
        java.util.Map<Long, java.util.Map<String, Object>> aggMap = new HashMap<>();
        for (java.util.Map<String, Object> row : aggRows) {
            Long rowId = getLong(row, "naturalProductId", "natural_product_id");
            if (rowId != null) {
                aggMap.put(rowId, row);
            }
        }

        List<NaturalProductDetailView> views = records.stream().map(np -> {
            NaturalProductDetailView view = new NaturalProductDetailView();
            BeanUtils.copyProperties(np, view);
            java.util.Map<String, Object> agg = aggMap.get(np.getId());
            if (agg != null) {
                view.setBioactivityCount(agg.get("bioactivityCount") == null ? null : ((Number) agg.get("bioactivityCount")).longValue());
                view.setTargetCount(agg.get("targetCount") == null ? null : ((Number) agg.get("targetCount")).longValue());
                view.setBestActivityValue(agg.get("bestActivityValue") == null ? null : new BigDecimal(String.valueOf(agg.get("bestActivityValue"))));
            } else {
                view.setBioactivityCount(0L);
                view.setTargetCount(0L);
                view.setBestActivityValue(null);
            }
            return view;
        }).collect(Collectors.toList());

        return ApiResponse.ok(new PageResponse<>(views, result.getCurrent(), result.getSize(), result.getTotal()));
    }

    @GetMapping("/{npId}")
    public ApiResponse<NaturalProductDetailView> detail(@PathVariable("npId") String npId) {
        NaturalProduct np = naturalProductService.getOne(
                new QueryWrapper<NaturalProduct>().eq("np_id", npId));
        if (np == null) {
            return ApiResponse.error(ApiCode.SUCCESS, "Not found");
        }
        NaturalProductDetailView view = new NaturalProductDetailView();
        BeanUtils.copyProperties(np, view);

        QueryWrapper<Bioactivity> aggWrapper = new QueryWrapper<>();
        aggWrapper.select(
                "COUNT(*) as bioactivityCount",
                "COUNT(DISTINCT target_id) as targetCount",
                "MIN(COALESCE(activity_value_std, activity_value)) as bestActivityValue"
        );
        aggWrapper.eq("natural_product_id", np.getId());
        java.util.Map<String, Object> agg = bioactivityService.getMap(aggWrapper);
        if (agg != null) {
            view.setBioactivityCount(agg.get("bioactivityCount") == null ? 0L : ((Number) agg.get("bioactivityCount")).longValue());
            view.setTargetCount(agg.get("targetCount") == null ? 0L : ((Number) agg.get("targetCount")).longValue());
            view.setBestActivityValue(agg.get("bestActivityValue") == null ? null : new BigDecimal(String.valueOf(agg.get("bestActivityValue"))));
        } else {
            view.setBioactivityCount(0L);
            view.setTargetCount(0L);
            view.setBestActivityValue(null);
        }

        QueryWrapper<BioResourceNaturalProduct> brCountWrapper = new QueryWrapper<>();
        brCountWrapper.select("COUNT(DISTINCT org_id) AS cnt");
        brCountWrapper.eq("np_id", np.getNpId());
        java.util.Map<String, Object> brCountRow = bioResourceNaturalProductService.getMap(brCountWrapper);
        Long bioResourceCount = brCountRow == null || brCountRow.get("cnt") == null
                ? 0L
                : ((Number) brCountRow.get("cnt")).longValue();
        view.setBioResourceCount(bioResourceCount);

        return ApiResponse.ok(view);
    }

    @GetMapping("/{npId}/bioactivity")
    public ApiResponse<PageResponse<Bioactivity>> bioactivity(
            @PathVariable("npId") String npId,
            @RequestParam(defaultValue = "1") long page,
            @RequestParam(defaultValue = "20") long pageSize
    ) {
        Long naturalProductId = resolveNaturalProductId(npId);
        if (naturalProductId == null) {
            return ApiResponse.error(ApiCode.SUCCESS, "Not found");
        }
        long safePage = page < 1 ? 1 : page;
        long safePageSize = pageSize < 1 ? 20 : Math.min(pageSize, MAX_PAGE_SIZE);
        Page<Bioactivity> mpPage = new Page<>(safePage, safePageSize);
        Page<Bioactivity> result = bioactivityService.page(mpPage,
                new QueryWrapper<Bioactivity>().eq("natural_product_id", naturalProductId));
        return ApiResponse.ok(PageResponse.from(result));
    }

    @GetMapping("/{npId}/targets")
    public ApiResponse<PageResponse<Target>> targets(
            @PathVariable("npId") String npId,
            @RequestParam(defaultValue = "1") long page,
            @RequestParam(defaultValue = "20") long pageSize
    ) {
        //验证分页参数
        long safePage = page < 1 ? 1 : page;
        long safePageSize = pageSize < 1 ? 20 : Math.min(pageSize, MAX_PAGE_SIZE);

        //解析天然产物ID
        Long naturalProductId = resolveNaturalProductId(npId);
        if (naturalProductId == null) {
            return ApiResponse.error(ApiCode.SUCCESS, "Not found");
        }
        //查询关联的靶点ID列表
        List<Long> targetIds = bioactivityService.list(
                        new QueryWrapper<Bioactivity>().select("distinct target_id")
                                .eq("natural_product_id", naturalProductId))
                .stream().map(Bioactivity::getTargetId).collect(Collectors.toList());
        if (targetIds.isEmpty()) {
            return ApiResponse.ok(PageResponse.from(new Page<>()));
        }

        //分页查询靶点信息
        Page<Target> mpPage = new Page<>(safePage, safePageSize);
        QueryWrapper<Target> wrapper = new QueryWrapper<Target>()
                .in("id", targetIds);
        Page<Target> result = targetService.page(mpPage, wrapper);
        return ApiResponse.ok(PageResponse.from(result));
    }

    @GetMapping("/{npId}/bioactivity-targets")
    public ApiResponse<List<BioactivityTargetSummary>> bioactivityTargets(@PathVariable("npId") String npId) {
        Long naturalProductId = resolveNaturalProductId(npId);
        if (naturalProductId == null) {
            return ApiResponse.error(ApiCode.SUCCESS, "Not found");
        }
        List<BioactivityTargetSummary> list = bioactivityMapper.listTargetSummaries(naturalProductId);
        return ApiResponse.ok(list == null ? Collections.emptyList() : list);
    }

    @GetMapping("/{npId}/bio-resources")
    public ApiResponse<PageResponse<BioResource>> bioResources(
            @PathVariable("npId") String npId,
            @RequestParam(defaultValue = "1") long page,
            @RequestParam(defaultValue = "20") long pageSize) {
        //验证分页参数
        long safePage = page < 1 ? 1 : page;
        long safePageSize = pageSize < 1 ? 20 : Math.min(pageSize, MAX_PAGE_SIZE);

        NaturalProduct np = naturalProductService.getOne(
                new QueryWrapper<NaturalProduct>().select("np_id").eq("np_id", npId));
        if (np == null) {
            return ApiResponse.error(ApiCode.SUCCESS, "Not found");
        }

        QueryWrapper<BioResourceNaturalProduct> countWrapper = new QueryWrapper<BioResourceNaturalProduct>()
                .eq("np_id", npId)
                .select("DISTINCT org_id");
        long total = bioResourceNaturalProductService.count(countWrapper);
        if (total == 0) {
            return ApiResponse.ok(PageResponse.from(new Page<>()));
        }

        Page<BioResourceNaturalProduct> pageRequest = new Page<>(safePage, safePageSize);
        QueryWrapper<BioResourceNaturalProduct> wrapper = new QueryWrapper<BioResourceNaturalProduct>()
                .eq("np_id", npId)
                .select("DISTINCT org_id")
                .orderByAsc("org_id");

        Page<BioResourceNaturalProduct> linkPage = bioResourceNaturalProductService.page(pageRequest, wrapper);
        List<String> resourceIds = linkPage.getRecords().stream()
                .map(BioResourceNaturalProduct::getOrgId)
                .filter(Objects::nonNull)
                .collect(Collectors.toList());
        if (resourceIds.isEmpty()) {
            return ApiResponse.ok(PageResponse.from(new Page<>()));
        }
        List<BioResource> resources = bioResourceService.list(
                new QueryWrapper<BioResource>().in("resource_id", resourceIds)
                        .orderByAsc("resource_id"));
        return ApiResponse.ok(new PageResponse<>(resources, safePage, safePageSize, total));
    }

    private Long resolveNaturalProductId(String npId) {
        NaturalProduct np = naturalProductService.getOne(
                new QueryWrapper<NaturalProduct>().select("id").eq("np_id", npId));
        return np == null ? null : np.getId();
    }

    private Long getLong(Map<String, Object> row, String... keys) {
        for (String key : keys) {
            Object value = row.get(key);
            if (value instanceof Number) {
                return ((Number) value).longValue();
            }
            if (value instanceof String && StringUtils.hasText((String) value)) {
                try {
                    return Long.parseLong(((String) value).trim());
                } catch (NumberFormatException ignored) {
                    // try next key
                }
            }
        }
        return null;
    }

    private String requireSafeLiteral(String input, String fieldName) {
        String value = input.trim();
        if (!SAFE_LITERAL.matcher(value).matches()) {
            throw new IllegalArgumentException(fieldName + " contains invalid characters");
        }
        return value;
    }
}
