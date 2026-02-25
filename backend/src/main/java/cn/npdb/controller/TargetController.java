package cn.npdb.controller;

import cn.npdb.common.ApiCode;
import cn.npdb.common.ApiResponse;
import cn.npdb.common.PageResponse;
import cn.npdb.dto.BioactivityWithNpId;
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
            @RequestParam(required = false) String targetType,
            @RequestParam(required = false) String bioclass
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
        if (StringUtils.hasText(bioclass)) {
            wrapper.eq("bioclass", bioclass.trim());
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
//        view.setNumOfNaturalProducts(target.getNumOfNaturalProducts());
        view.setCreatedAt(target.getCreatedAt());
        view.setUpdatedAt(target.getUpdatedAt());

        java.util.Map<String, Object> agg = bioactivityService.getMap(
                new QueryWrapper<Bioactivity>()
                        .select(
                                "COUNT(DISTINCT natural_product_id) as naturalproductcount",
                                "COUNT(*) as bioactivitycount",
                                "MIN(COALESCE(activity_value_std, activity_value)) as bestactivityvalue"
                        )
                        .eq("target_id", target.getId())
        );
        if (agg != null) {
            view.setNaturalProductCount(agg.get("naturalproductcount") == null ? 0L : ((Number) agg.get("naturalproductcount")).longValue());
            view.setBioactivityCount(agg.get("bioactivitycount") == null ? 0L : ((Number) agg.get("bioactivitycount")).longValue());
            view.setBestActivityValue(agg.get("bestactivityvalue") == null ? null : new java.math.BigDecimal(String.valueOf(agg.get("bestactivityvalue"))));
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


    @GetMapping("/{targetId}/bioactivity")
    public ApiResponse<PageResponse<BioactivityWithNpId>> bioactivity(
            @PathVariable("targetId") String targetId,
            @RequestParam(defaultValue = "1") long page,
            @RequestParam(defaultValue = "20") long pageSize
    ) {
        long safePage = page < 1 ? 1 : page;
        long safePageSize = pageSize < 1 ? 20 : Math.min(pageSize, MAX_PAGE_SIZE);
        Target target = targetService.getOne(new QueryWrapper<Target>().select("id").eq("target_id", targetId));
        if (target == null) {
            return ApiResponse.error(ApiCode.SUCCESS, "Not found");
        }
        Page<BioactivityWithNpId> mpPage = new Page<>(safePage, safePageSize);
        Page<BioactivityWithNpId> result = ((cn.npdb.mapper.BioactivityMapper) bioactivityService.getBaseMapper())
                .listByTargetWithNpId(mpPage, target.getId());
        return ApiResponse.ok(PageResponse.from(result));
    }

    /**
     * @description 获取靶点类型列表
     * @return
     */
    @GetMapping("/targetTypes")
    public ApiResponse<List<String>> targetTypes() {
        List<String> types = targetService.list()
                .stream()
                .map(Target::getTargetType)
                .filter(StringUtils::hasText)
                .distinct()
                .sorted()  // 升序排序
                .collect(Collectors.toList());
        return ApiResponse.ok(types);
    }

    /**
     * @description 获取靶点生物分类列表
     * @return
     */
    @GetMapping("/bioclasses")
    public ApiResponse<List<String>> bioclassList() {
        List<String> bioclasses = targetService.list()
                .stream()
                .map(Target::getBioclass)
                .filter(StringUtils::hasText)
                .distinct()
                .sorted()  // 升序排序
                .collect(Collectors.toList());
        return ApiResponse.ok(bioclasses);
    }
}
