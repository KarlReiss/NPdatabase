package cn.npdb.controller;

import cn.npdb.common.ApiCode;
import cn.npdb.common.ApiResponse;
import cn.npdb.common.PageResponse;
import cn.npdb.entity.Bioactivity;
import cn.npdb.entity.NaturalProductDetailView;
import cn.npdb.entity.Target;
import cn.npdb.entity.TargetDetailView;
import cn.npdb.mapper.NaturalProductDetailMapper;
import cn.npdb.service.BioactivityService;
import cn.npdb.service.TargetService;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/targets")
public class TargetController {
    private static final long MAX_PAGE_SIZE = 200;

    private final TargetService targetService;
    private final BioactivityService bioactivityService;
    private final NaturalProductDetailMapper naturalProductDetailMapper;

    public TargetController(TargetService targetService,
                            BioactivityService bioactivityService,
                            NaturalProductDetailMapper naturalProductDetailMapper) {
        this.targetService = targetService;
        this.bioactivityService = bioactivityService;
        this.naturalProductDetailMapper = naturalProductDetailMapper;
    }

    @GetMapping
    public ApiResponse<PageResponse<Target>> list(
            @RequestParam(defaultValue = "1") long page,
            @RequestParam(defaultValue = "20") long pageSize,
            @RequestParam(required = false) String q,
            @RequestParam(required = false) String targetType
    ) {
        long safePage = page < 1 ? 1 : page;
        long safePageSize = pageSize < 1 ? 20 : Math.min(pageSize, MAX_PAGE_SIZE);

        QueryWrapper<Target> wrapper = new QueryWrapper<>();
        if (StringUtils.hasText(q)) {
            wrapper.and(w -> w.like("target_name", q)
                    .or().like("target_id", q));
        }
        if (StringUtils.hasText(targetType)) {
            wrapper.eq("target_type", targetType.trim());
        }
        wrapper.orderByDesc("id");

        Page<Target> mpPage = new Page<>(safePage, safePageSize);
        Page<Target> result = targetService.page(mpPage, wrapper);
        return ApiResponse.ok(PageResponse.from(result));
    }

    @GetMapping("/{targetId}")
    public ApiResponse<TargetDetailView> detail(@PathVariable("targetId") String targetId) {
        Target target = targetService.getOne(
                new QueryWrapper<Target>().eq("target_id", targetId));
        if (target == null) {
            return ApiResponse.error(ApiCode.SUCCESS, "Not found");
        }
        TargetDetailView view = new TargetDetailView();
        view.setId(target.getId());
        view.setTargetId(target.getTargetId());
        view.setTargetType(target.getTargetType());
        view.setTargetName(target.getTargetName());
        view.setTargetOrganism(target.getTargetOrganism());
        view.setTargetOrganismTaxId(target.getTargetOrganismTaxId());
        view.setUniprotId(target.getUniprotId());
        view.setGeneName(target.getGeneName());
        view.setSynonyms(target.getSynonyms());
        view.setFunction(target.getFunction());
        view.setPdbStructure(target.getPdbStructure());
        view.setBioclass(target.getBioclass());
        view.setEcNumber(target.getEcNumber());
        view.setSequence(target.getSequence());
        view.setTtdId(target.getTtdId());
        view.setNumOfActivities(target.getNumOfActivities());
        view.setNumOfNaturalProducts(target.getNumOfNaturalProducts());
        view.setCreatedAt(target.getCreatedAt());
        view.setUpdatedAt(target.getUpdatedAt());

        java.util.Map<String, Object> agg = bioactivityService.getMap(
                new QueryWrapper<Bioactivity>()
                        .select(
                                "COUNT(DISTINCT natural_product_id) as naturalProductCount",
                                "COUNT(*) as bioactivityCount",
                                "MIN(activity_value_std) as bestActivityValue"
                        )
                        .eq("target_id", target.getId())
        );
        if (agg != null) {
            view.setNaturalProductCount(agg.get("naturalProductCount") == null ? 0L : ((Number) agg.get("naturalProductCount")).longValue());
            view.setBioactivityCount(agg.get("bioactivityCount") == null ? 0L : ((Number) agg.get("bioactivityCount")).longValue());
            view.setBestActivityValue(agg.get("bestActivityValue") == null ? null : new java.math.BigDecimal(String.valueOf(agg.get("bestActivityValue"))));
        } else {
            view.setNaturalProductCount(0L);
            view.setBioactivityCount(0L);
            view.setBestActivityValue(null);
        }
        return ApiResponse.ok(view);
    }

    @GetMapping("/{targetId}/natural-products")
    public ApiResponse<PageResponse<NaturalProductDetailView>> naturalProducts(
            @PathVariable("targetId") String targetId,
            @RequestParam(defaultValue = "1") long page,
            @RequestParam(defaultValue = "20") long pageSize
    ) {
        //验证分页参数
        long safePage = page < 1 ? 1 : page;
        long safePageSize = pageSize < 1 ? 20 : Math.min(pageSize, MAX_PAGE_SIZE);
        //查询靶点
        Target target = targetService.getOne(new QueryWrapper<Target>().select("id").eq("target_id", targetId));
        if (target == null) {
            return ApiResponse.error(ApiCode.SUCCESS, "Not found");
        }
        //查询关联的自然产物ID列表
        List<Long> npIds = bioactivityService.list(
                        new QueryWrapper<Bioactivity>().select("distinct natural_product_id")
                                .eq("target_id", target.getId()))
                .stream().map(Bioactivity::getNaturalProductId).collect(Collectors.toList());
        if (npIds.isEmpty()) {
            return ApiResponse.ok(PageResponse.from(new Page<>()));
        }
        //分页查询自然产物列表
        Page<NaturalProductDetailView> mpPage = new Page<>(safePage, safePageSize);
        QueryWrapper<NaturalProductDetailView> wrapper = new QueryWrapper<NaturalProductDetailView>()
                .in("id", npIds);
        Page<NaturalProductDetailView> result = naturalProductDetailMapper.selectPage(mpPage, wrapper);
        return ApiResponse.ok(PageResponse.from(result));
    }
}
