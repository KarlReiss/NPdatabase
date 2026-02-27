package cn.npdb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@TableName("v_target_detail")
public class TargetDetailView {
    @TableId(type = IdType.AUTO)
    private Long id;

    private String targetId;
    private String targetType;
    private String targetName;

    private String targetOrganism;
    private String targetOrganismTaxId;

    private String uniprotId;

    private Integer numOfActivities;
    private Integer numOfCompounds;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    private Long naturalProductCount;
    private Long bioactivityCount;
    private BigDecimal bestActivityValue;
}
