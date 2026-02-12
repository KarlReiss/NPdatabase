package cn.npdb.dto;

import lombok.Data;

import java.math.BigDecimal;

@Data
public class BioactivityTargetSummary {
    private Long targetDbId;
    private String targetId;
    private String targetName;
    private String targetType;
    private String targetOrganism;
    private String uniprotId;
    private Long bioactivityCount;
    private BigDecimal bestActivityValue;
}
