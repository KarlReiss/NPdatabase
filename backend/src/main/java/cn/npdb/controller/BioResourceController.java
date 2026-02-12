package cn.npdb.controller;

import cn.npdb.common.ApiCode;
import cn.npdb.common.ApiResponse;
import cn.npdb.common.PageResponse;
import cn.npdb.dto.BioResourceNaturalProductItem;
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
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
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
    public ApiResponse<List<BioResourceNaturalProductItem>> naturalProducts(@PathVariable("resourceId") String resourceId) {
        BioResource resource = bioResourceService.getOne(
                new QueryWrapper<BioResource>().select("resource_id").eq("resource_id", resourceId));
        if (resource == null) {
            return ApiResponse.error(ApiCode.NOT_FOUND, "Not found");
        }

        List<BioResourceNaturalProduct> links = bioResourceNaturalProductService.list(
                new QueryWrapper<BioResourceNaturalProduct>().eq("org_id", resourceId));
        if (links.isEmpty()) {
            return ApiResponse.ok(Collections.emptyList());
        }

        Map<String, Aggregate> aggregates = new LinkedHashMap<>();
        for (BioResourceNaturalProduct link : links) {
            if (link.getNpId() == null || link.getNpId().trim().isEmpty()) {
                continue;
            }
            Aggregate agg = aggregates.computeIfAbsent(link.getNpId().trim(), key -> new Aggregate());
            agg.sourceCount++;
            agg.orgIsolationPart.add(trimOrNull(link.getOrgIsolationPart()));
            agg.orgCollectLocation.add(trimOrNull(link.getOrgCollectLocation()));
            agg.orgCollectTime.add(trimOrNull(link.getOrgCollectTime()));
            agg.refType.add(trimOrNull(link.getRefType()));
            agg.refId.add(trimOrNull(link.getRefId()));
            agg.refIdType.add(trimOrNull(link.getRefIdType()));
            agg.refUrl.add(trimOrNull(link.getRefUrl()));
            agg.newCpFound.add(trimOrNull(link.getNewCpFound()));
        }

        if (aggregates.isEmpty()) {
            return ApiResponse.ok(Collections.emptyList());
        }

        List<String> npIds = aggregates.keySet().stream().collect(Collectors.toList());
        List<NaturalProduct> products = naturalProductService.list(
                new QueryWrapper<NaturalProduct>().in("np_id", npIds));
        Map<String, NaturalProduct> productMap = products.stream()
                .collect(Collectors.toMap(NaturalProduct::getNpId, p -> p, (a, b) -> a));

        List<BioResourceNaturalProductItem> items = npIds.stream().map(npId -> {
            Aggregate agg = aggregates.get(npId);
            NaturalProduct np = productMap.get(npId);
            BioResourceNaturalProductItem item = new BioResourceNaturalProductItem();
            item.setNpId(npId);
            if (np != null) {
                item.setPrefName(np.getPrefName());
                item.setIupacName(np.getIupacName());
                item.setMolecularWeight(np.getMolecularWeight());
                item.setXlogp(np.getXlogp());
                item.setPsa(np.getPsa());
                item.setFormula(np.getFormula());
            }
            item.setOrgIsolationPart(joinNonBlank(agg.orgIsolationPart));
            item.setOrgCollectLocation(joinNonBlank(agg.orgCollectLocation));
            item.setOrgCollectTime(joinNonBlank(agg.orgCollectTime));
            item.setRefType(joinNonBlank(agg.refType));
            item.setRefId(joinNonBlank(agg.refId));
            item.setRefIdType(joinNonBlank(agg.refIdType));
            item.setRefUrl(joinNonBlank(agg.refUrl));
            item.setNewCpFound(joinNonBlank(agg.newCpFound));
            item.setSourceCount(agg.sourceCount);
            return item;
        }).collect(Collectors.toList());

        return ApiResponse.ok(items);
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

    private static String joinNonBlank(Set<String> values) {
        String joined = values.stream()
                .filter(value -> value != null && !value.isEmpty())
                .distinct()
                .collect(Collectors.joining("; "));
        return joined.isEmpty() ? null : joined;
    }

    private static String trimOrNull(String value) {
        if (value == null) {
            return null;
        }
        String trimmed = value.trim();
        return trimmed.isEmpty() ? null : trimmed;
    }

    private static class Aggregate {
        private int sourceCount = 0;
        private final Set<String> orgIsolationPart = new LinkedHashSet<>();
        private final Set<String> orgCollectLocation = new LinkedHashSet<>();
        private final Set<String> orgCollectTime = new LinkedHashSet<>();
        private final Set<String> refType = new LinkedHashSet<>();
        private final Set<String> refId = new LinkedHashSet<>();
        private final Set<String> refIdType = new LinkedHashSet<>();
        private final Set<String> refUrl = new LinkedHashSet<>();
        private final Set<String> newCpFound = new LinkedHashSet<>();
    }
}
