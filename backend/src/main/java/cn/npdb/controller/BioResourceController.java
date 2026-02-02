package cn.npdb.controller;

import cn.npdb.common.ApiCode;
import cn.npdb.common.ApiResponse;
import cn.npdb.common.PageResponse;
import cn.npdb.entity.BioResource;
import cn.npdb.entity.BioResourceNaturalProduct;
import cn.npdb.entity.NaturalProduct;
import cn.npdb.entity.Prescription;
import cn.npdb.entity.PrescriptionResource;
import cn.npdb.service.BioResourceNaturalProductService;
import cn.npdb.service.BioResourceService;
import cn.npdb.service.NaturalProductService;
import cn.npdb.service.PrescriptionResourceService;
import cn.npdb.service.PrescriptionService;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/bio-resources")
public class BioResourceController {
    private static final long MAX_PAGE_SIZE = 200;

    private final BioResourceService bioResourceService;
    private final BioResourceNaturalProductService bioResourceNaturalProductService;
    private final NaturalProductService naturalProductService;
    private final PrescriptionResourceService prescriptionResourceService;
    private final PrescriptionService prescriptionService;

    public BioResourceController(BioResourceService bioResourceService,
                                 BioResourceNaturalProductService bioResourceNaturalProductService,
                                 NaturalProductService naturalProductService,
                                 PrescriptionResourceService prescriptionResourceService,
                                 PrescriptionService prescriptionService) {
        this.bioResourceService = bioResourceService;
        this.bioResourceNaturalProductService = bioResourceNaturalProductService;
        this.naturalProductService = naturalProductService;
        this.prescriptionResourceService = prescriptionResourceService;
        this.prescriptionService = prescriptionService;
    }

    @GetMapping
    public ApiResponse<PageResponse<BioResource>> list(
            @RequestParam(defaultValue = "1") long page,
            @RequestParam(defaultValue = "20") long pageSize,
            @RequestParam(required = false) String q,
            @RequestParam(required = false) String resourceType
    ) {
        long safePage = page < 1 ? 1 : page;
        long safePageSize = pageSize < 1 ? 20 : Math.min(pageSize, MAX_PAGE_SIZE);

        QueryWrapper<BioResource> wrapper = new QueryWrapper<>();
        if (StringUtils.hasText(q)) {
            wrapper.and(w -> w.like("chinese_name", q)
                    .or().like("latin_name", q)
                    .or().like("resource_id", q));
        }
        if (StringUtils.hasText(resourceType)) {
            wrapper.eq("resource_type", resourceType.trim());
        }
        wrapper.orderByDesc("id");

        Page<BioResource> mpPage = new Page<>(safePage, safePageSize);
        Page<BioResource> result = bioResourceService.page(mpPage, wrapper);
        return ApiResponse.ok(PageResponse.from(result));
    }

    @GetMapping("/{resourceId}")
    public ApiResponse<BioResource> detail(@PathVariable("resourceId") String resourceId) {
        BioResource resource = bioResourceService.getOne(
                new QueryWrapper<BioResource>().eq("resource_id", resourceId));
        if (resource == null) {
            return ApiResponse.error(ApiCode.NOT_FOUND, "Not found");
        }
        return ApiResponse.ok(resource);
    }

    @GetMapping("/{resourceId}/natural-products")
    public ApiResponse<List<NaturalProduct>> naturalProducts(@PathVariable("resourceId") String resourceId) {
        BioResource resource = bioResourceService.getOne(
                new QueryWrapper<BioResource>().select("id").eq("resource_id", resourceId));
        if (resource == null) {
            return ApiResponse.error(ApiCode.NOT_FOUND, "Not found");
        }
        List<Long> npIds = bioResourceNaturalProductService.list(
                        new QueryWrapper<BioResourceNaturalProduct>()
                                .select("distinct natural_product_id")
                                .eq("bio_resource_id", resource.getId()))
                .stream()
                .map(BioResourceNaturalProduct::getNaturalProductId)
                .collect(Collectors.toList());
        if (npIds.isEmpty()) {
            return ApiResponse.ok(Collections.emptyList());
        }
        List<NaturalProduct> list = naturalProductService.list(
                new QueryWrapper<NaturalProduct>().in("id", npIds));
        return ApiResponse.ok(list);
    }

    @GetMapping("/{resourceId}/prescriptions")
    public ApiResponse<List<Prescription>> prescriptions(@PathVariable("resourceId") String resourceId) {
        BioResource resource = bioResourceService.getOne(
                new QueryWrapper<BioResource>().select("id").eq("resource_id", resourceId));
        if (resource == null) {
            return ApiResponse.error(ApiCode.NOT_FOUND, "Not found");
        }
        List<Long> prescriptionIds = prescriptionResourceService.list(
                        new QueryWrapper<PrescriptionResource>()
                                .select("distinct prescription_id")
                                .eq("bio_resource_id", resource.getId()))
                .stream()
                .map(PrescriptionResource::getPrescriptionId)
                .collect(Collectors.toList());
        if (prescriptionIds.isEmpty()) {
            return ApiResponse.ok(Collections.emptyList());
        }
        List<Prescription> list = prescriptionService.list(
                new QueryWrapper<Prescription>().in("id", prescriptionIds));
        return ApiResponse.ok(list);
    }
}
