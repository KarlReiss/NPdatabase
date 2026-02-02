package cn.npdb.controller;

import cn.npdb.common.ApiResponse;
import cn.npdb.dto.StatsResponse;
import cn.npdb.service.BioResourceService;
import cn.npdb.service.BioactivityService;
import cn.npdb.service.DiseaseService;
import cn.npdb.service.NaturalProductService;
import cn.npdb.service.PrescriptionService;
import cn.npdb.service.TargetService;
import cn.npdb.service.ToxicityService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class StatsController {
    private final NaturalProductService naturalProductService;
    private final TargetService targetService;
    private final BioactivityService bioactivityService;
    private final ToxicityService toxicityService;
    private final BioResourceService bioResourceService;
    private final PrescriptionService prescriptionService;
    private final DiseaseService diseaseService;

    public StatsController(NaturalProductService naturalProductService,
                           TargetService targetService,
                           BioactivityService bioactivityService,
                           ToxicityService toxicityService,
                           BioResourceService bioResourceService,
                           PrescriptionService prescriptionService,
                           DiseaseService diseaseService) {
        this.naturalProductService = naturalProductService;
        this.targetService = targetService;
        this.bioactivityService = bioactivityService;
        this.toxicityService = toxicityService;
        this.bioResourceService = bioResourceService;
        this.prescriptionService = prescriptionService;
        this.diseaseService = diseaseService;
    }

    @GetMapping("/stats")
    public ApiResponse<StatsResponse> stats() {
        StatsResponse resp = new StatsResponse(
                naturalProductService.count(),
                targetService.count(),
                bioactivityService.count(),
                toxicityService.count(),
                bioResourceService.count(),
                prescriptionService.count(),
                diseaseService.count()
        );
        return ApiResponse.ok(resp);
    }
}
