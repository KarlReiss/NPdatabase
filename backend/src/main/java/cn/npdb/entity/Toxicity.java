package cn.npdb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@TableName("toxicity")
public class Toxicity {
    @TableId(type = IdType.AUTO)
    private Long id;

    private Long naturalProductId;

    private String toxicityType;
    private BigDecimal toxicityValue;
    private String toxicityUnits;
    private String dose;
    private String symptoms;

    private String assayOrganism;
    private String assayMethod;

    private String refId;
    private String refIdType;

    private LocalDateTime createdAt;
}
