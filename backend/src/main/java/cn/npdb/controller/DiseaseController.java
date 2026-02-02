package cn.npdb.controller;

import cn.npdb.common.ApiCode;
import cn.npdb.common.ApiResponse;
import cn.npdb.common.PageResponse;
import cn.npdb.entity.BioResource;
import cn.npdb.entity.BioResourceDiseaseAssociation;
import cn.npdb.entity.BioResourceNaturalProduct;
import cn.npdb.entity.Disease;
import cn.npdb.entity.NaturalProduct;
import cn.npdb.service.BioResourceDiseaseAssociationService;
import cn.npdb.service.BioResourceNaturalProductService;
import cn.npdb.service.BioResourceService;
import cn.npdb.service.DiseaseService;
import cn.npdb.service.NaturalProductService;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/diseases")
public class DiseaseController {
    private static final long MAX_PAGE_SIZE = 200;

    private final DiseaseService diseaseService;
    private final BioResourceDiseaseAssociationService bioResourceDiseaseAssociationService;
    private final BioResourceService bioResourceService;
    private final BioResourceNaturalProductService bioResourceNaturalProductService;
    private final NaturalProductService naturalProductService;

    public DiseaseController(DiseaseService diseaseService,
                             BioResourceDiseaseAssociationService bioResourceDiseaseAssociationService,
                             BioResourceService bioResourceService,
                             BioResourceNaturalProductService bioResourceNaturalProductService,
                             NaturalProductService naturalProductService) {
        this.diseaseService = diseaseService;
        this.bioResourceDiseaseAssociationService = bioResourceDiseaseAssociationService;
        this.bioResourceService = bioResourceService;
        this.bioResourceNaturalProductService = bioResourceNaturalProductService;
        this.naturalProductService = naturalProductService;
    }

    @GetMapping
    public ApiResponse<PageResponse<Disease>> list(
            @RequestParam(defaultValue = "1") long page,
            @RequestParam(defaultValue = "20") long pageSize,
            @RequestParam(required = false) String q,
            @RequestParam(required = false) String category
    ) {
        long safePage = page < 1 ? 1 : page;
        long safePageSize = pageSize < 1 ? 20 : Math.min(pageSize, MAX_PAGE_SIZE);

        QueryWrapper<Disease> wrapper = new QueryWrapper<>();
        if (StringUtils.hasText(q)) {
            wrapper.and(w -> w.like("disease_name", q)
                    .or().like("disease_name_zh", q)
                    .or().like("disease_id", q)
                    .or().like("icd11_code", q));
        }
        if (StringUtils.hasText(category)) {
            wrapper.eq("disease_category", category.trim());
        }
        wrapper.orderByDesc("id");

        Page<Disease> mpPage = new Page<>(safePage, safePageSize);
        Page<Disease> result = diseaseService.page(mpPage, wrapper);
        return ApiResponse.ok(PageResponse.from(result));
    }

    @GetMapping("/{diseaseId}")
    public ApiResponse<Disease> detail(@PathVariable("diseaseId") String diseaseId) {
        Disease disease = diseaseService.getOne(
                new QueryWrapper<Disease>().eq("disease_id", diseaseId));
        if (disease == null) {
            return ApiResponse.error(ApiCode.NOT_FOUND, "Not found");
        }
        return ApiResponse.ok(disease);
    }

    @GetMapping("/{diseaseId}/bio-resources")
    public ApiResponse<List<BioResource>> bioResources(@PathVariable("diseaseId") String diseaseId) {
        Disease disease = diseaseService.getOne(
                new QueryWrapper<Disease>().select("id").eq("disease_id", diseaseId));
        if (disease == null) {
            return ApiResponse.error(ApiCode.NOT_FOUND, "Not found");
        }
        List<Long> resourceIds = bioResourceDiseaseAssociationService.list(
                        new QueryWrapper<BioResourceDiseaseAssociation>()
                                .select("distinct bio_resource_id")
                                .eq("disease_id", disease.getId()))
                .stream()
                .map(BioResourceDiseaseAssociation::getBioResourceId)
                .collect(Collectors.toList());
        if (resourceIds.isEmpty()) {
            return ApiResponse.ok(Collections.emptyList());
        }
        List<BioResource> list = bioResourceService.list(
                new QueryWrapper<BioResource>().in("id", resourceIds));
        return ApiResponse.ok(list);
    }

    @GetMapping("/{diseaseId}/natural-products")
    public ApiResponse<List<NaturalProduct>> naturalProducts(@PathVariable("diseaseId") String diseaseId) {
        Disease disease = diseaseService.getOne(
                new QueryWrapper<Disease>().select("id").eq("disease_id", diseaseId));
        if (disease == null) {
            return ApiResponse.error(ApiCode.NOT_FOUND, "Not found");
        }
        List<Long> resourceIds = bioResourceDiseaseAssociationService.list(
                        new QueryWrapper<BioResourceDiseaseAssociation>()
                                .select("distinct bio_resource_id")
                                .eq("disease_id", disease.getId()))
                .stream()
                .map(BioResourceDiseaseAssociation::getBioResourceId)
                .collect(Collectors.toList());
        if (resourceIds.isEmpty()) {
            return ApiResponse.ok(Collections.emptyList());
        }
        Set<Long> npIds = new HashSet<>(
                bioResourceNaturalProductService.list(
                                new QueryWrapper<BioResourceNaturalProduct>()
                                        .select("distinct natural_product_id")
                                        .in("bio_resource_id", resourceIds))
                        .stream()
                        .map(BioResourceNaturalProduct::getNaturalProductId)
                        .collect(Collectors.toSet())
        );
        if (npIds.isEmpty()) {
            return ApiResponse.ok(Collections.emptyList());
        }
        List<NaturalProduct> list = naturalProductService.list(
                new QueryWrapper<NaturalProduct>().in("id", npIds));
        return ApiResponse.ok(list);
    }
}
