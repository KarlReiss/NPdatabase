package cn.npdb.controller;

import cn.npdb.common.ApiCode;
import cn.npdb.common.ApiResponse;
import cn.npdb.common.PageResponse;
import cn.npdb.entity.BioResource;
import cn.npdb.entity.NaturalProduct;
import cn.npdb.entity.Prescription;
import cn.npdb.entity.PrescriptionNaturalProduct;
import cn.npdb.entity.PrescriptionResource;
import cn.npdb.service.BioResourceService;
import cn.npdb.service.NaturalProductService;
import cn.npdb.service.PrescriptionNaturalProductService;
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
@RequestMapping("/api/prescriptions")
public class PrescriptionController {
    private static final long MAX_PAGE_SIZE = 200;

    private final PrescriptionService prescriptionService;
    private final PrescriptionResourceService prescriptionResourceService;
    private final PrescriptionNaturalProductService prescriptionNaturalProductService;
    private final BioResourceService bioResourceService;
    private final NaturalProductService naturalProductService;

    public PrescriptionController(PrescriptionService prescriptionService,
                                  PrescriptionResourceService prescriptionResourceService,
                                  PrescriptionNaturalProductService prescriptionNaturalProductService,
                                  BioResourceService bioResourceService,
                                  NaturalProductService naturalProductService) {
        this.prescriptionService = prescriptionService;
        this.prescriptionResourceService = prescriptionResourceService;
        this.prescriptionNaturalProductService = prescriptionNaturalProductService;
        this.bioResourceService = bioResourceService;
        this.naturalProductService = naturalProductService;
    }

    @GetMapping
    public ApiResponse<PageResponse<Prescription>> list(
            @RequestParam(defaultValue = "1") long page,
            @RequestParam(defaultValue = "20") long pageSize,
            @RequestParam(required = false) String q,
            @RequestParam(required = false) String category
    ) {
        long safePage = page < 1 ? 1 : page;
        long safePageSize = pageSize < 1 ? 20 : Math.min(pageSize, MAX_PAGE_SIZE);

        QueryWrapper<Prescription> wrapper = new QueryWrapper<>();
        if (StringUtils.hasText(q)) {
            wrapper.and(w -> w.like("chinese_name", q)
                    .or().like("prescription_id", q)
                    .or().like("pinyin_name", q));
        }
        if (StringUtils.hasText(category)) {
            wrapper.eq("category", category.trim());
        }
        wrapper.orderByDesc("id");

        Page<Prescription> mpPage = new Page<>(safePage, safePageSize);
        Page<Prescription> result = prescriptionService.page(mpPage, wrapper);
        return ApiResponse.ok(PageResponse.from(result));
    }

    @GetMapping("/{prescriptionId}")
    public ApiResponse<Prescription> detail(@PathVariable("prescriptionId") String prescriptionId) {
        Prescription prescription = prescriptionService.getOne(
                new QueryWrapper<Prescription>().eq("prescription_id", prescriptionId));
        if (prescription == null) {
            return ApiResponse.error(ApiCode.NOT_FOUND, "Not found");
        }
        return ApiResponse.ok(prescription);
    }

    @GetMapping("/{prescriptionId}/bio-resources")
    public ApiResponse<List<BioResource>> bioResources(@PathVariable("prescriptionId") String prescriptionId) {
        Prescription prescription = prescriptionService.getOne(
                new QueryWrapper<Prescription>().select("id").eq("prescription_id", prescriptionId));
        if (prescription == null) {
            return ApiResponse.error(ApiCode.NOT_FOUND, "Not found");
        }
        List<Long> resourceIds = prescriptionResourceService.list(
                        new QueryWrapper<PrescriptionResource>()
                                .select("distinct bio_resource_id")
                                .eq("prescription_id", prescription.getId()))
                .stream()
                .map(PrescriptionResource::getBioResourceId)
                .collect(Collectors.toList());
        if (resourceIds.isEmpty()) {
            return ApiResponse.ok(Collections.emptyList());
        }
        List<BioResource> list = bioResourceService.list(
                new QueryWrapper<BioResource>().in("id", resourceIds));
        return ApiResponse.ok(list);
    }

    @GetMapping("/{prescriptionId}/natural-products")
    public ApiResponse<List<NaturalProduct>> naturalProducts(@PathVariable("prescriptionId") String prescriptionId) {
        Prescription prescription = prescriptionService.getOne(
                new QueryWrapper<Prescription>().select("id").eq("prescription_id", prescriptionId));
        if (prescription == null) {
            return ApiResponse.error(ApiCode.NOT_FOUND, "Not found");
        }
        List<Long> npIds = prescriptionNaturalProductService.list(
                        new QueryWrapper<PrescriptionNaturalProduct>()
                                .select("distinct natural_product_id")
                                .eq("prescription_id", prescription.getId()))
                .stream()
                .map(PrescriptionNaturalProduct::getNaturalProductId)
                .collect(Collectors.toList());
        if (npIds.isEmpty()) {
            return ApiResponse.ok(Collections.emptyList());
        }
        List<NaturalProduct> list = naturalProductService.list(
                new QueryWrapper<NaturalProduct>().in("id", npIds));
        return ApiResponse.ok(list);
    }
}
