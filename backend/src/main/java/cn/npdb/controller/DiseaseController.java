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

        String keyword = StringUtils.hasText(q) ? q.trim() : null;
        String categoryValue = StringUtils.hasText(category) ? category.trim() : null;
        Page<Disease> result = diseaseService.listPage(safePage, safePageSize, keyword, categoryValue);
        return ApiResponse.ok(PageResponse.from(result));
    }

    @GetMapping("/{diseaseId}")
    public ApiResponse<Disease> detail(@PathVariable("diseaseId") Long diseaseId) {
        Disease disease = diseaseService.getById(diseaseId);
        if (disease == null) {
            return ApiResponse.error(ApiCode.NOT_FOUND, "Not found");
        }
        return ApiResponse.ok(disease);
    }

    @GetMapping("/{diseaseId}/bio-resources")
    public ApiResponse<PageResponse<BioResource>> bioResources(
            @PathVariable("diseaseId") Long diseaseId,
            @RequestParam(defaultValue = "1") long page,
            @RequestParam(defaultValue = "20") long pageSize
    ) {
        //验证分页参数
        long safePage = page < 1 ? 1 : page;
        long safePageSize = pageSize < 1 ? 20 : Math.min(pageSize, MAX_PAGE_SIZE);
        //验证疾病是否存在
        Disease disease = diseaseService.getById(diseaseId);
        if (disease == null) {
            return ApiResponse.error(ApiCode.NOT_FOUND, "Not found");
        }
        //查询关联的生物资源ID
        List<Long> resourceIds = bioResourceDiseaseAssociationService.list(
                        new QueryWrapper<BioResourceDiseaseAssociation>()
                                .select("distinct bio_resource_id")
                                .eq("disease_id", diseaseId))
                .stream()
                .map(BioResourceDiseaseAssociation::getBioResourceId)
                .collect(Collectors.toList());
        if (resourceIds.isEmpty()) {
            return ApiResponse.ok(PageResponse.from(new Page<>()));
        }
        //分页查询生物资源列表
        Page<BioResource> mpPage = new Page<>(safePage, safePageSize);
        Page<BioResource> result = bioResourceService.page(mpPage,
                new QueryWrapper<BioResource>().in("id", resourceIds).orderByDesc("id"));
        return ApiResponse.ok(PageResponse.from(result));
    }

    @GetMapping("/{diseaseId}/natural-products")
    public ApiResponse<PageResponse<NaturalProduct>> naturalProducts(
            @PathVariable("diseaseId") Long diseaseId,
            @RequestParam(defaultValue = "1") long page,
            @RequestParam(defaultValue = "20") long pageSize
    ) {
        //验证分页参数
        long safePage = page < 1 ? 1 : page;
        long safePageSize = pageSize < 1 ? 20 : Math.min(pageSize, MAX_PAGE_SIZE);
        //验证疾病是否存在
        Disease disease = diseaseService.getById(diseaseId);
        if (disease == null) {
            return ApiResponse.error(ApiCode.NOT_FOUND, "Not found");
        }
        //查询关联的生物资源ID
        List<Long> resourceIds = bioResourceDiseaseAssociationService.list(
                        new QueryWrapper<BioResourceDiseaseAssociation>()
                                .select("distinct bio_resource_id")
                                .eq("disease_id", diseaseId))
                .stream()
                .map(BioResourceDiseaseAssociation::getBioResourceId)
                .collect(Collectors.toList());
        if (resourceIds.isEmpty()) {
            return ApiResponse.ok(PageResponse.from(new Page<>()));
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
            return ApiResponse.ok(PageResponse.from(new Page<>()));
        }
        Page<NaturalProduct> mpPage = new Page<>(safePage, safePageSize);
        Page<NaturalProduct> result = naturalProductService.page(mpPage,
                new QueryWrapper<NaturalProduct>().in("id", npIds).orderByDesc("id"));
        return ApiResponse.ok(PageResponse.from(result));
    }
}
