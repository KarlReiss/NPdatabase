package cn.npdb.dto;

import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
public class BioactivityWithNpId {
    private Long id;
    private Long naturalProductId;
    private String npId;
    private Long targetId;
    private String activityType;
    private String activityTypeGrouped;
    private String activityRelation;
    private BigDecimal activityValue;
    private String activityUnits;
    private BigDecimal activityValueStd;
    private String activityUnitsStd;
    private String assayOrganism;
    private String assayTaxId;
    private String assayStrain;
    private String assayTissue;
    private String assayCellType;
    private String refId;
    private String refIdType;
    private LocalDateTime createdAt;
}
