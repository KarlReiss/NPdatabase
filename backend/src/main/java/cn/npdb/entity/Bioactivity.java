package cn.npdb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@TableName("bioactivity")
public class Bioactivity {
    @TableId(type = IdType.AUTO)
    private Long id;

    private Long naturalProductId;
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
