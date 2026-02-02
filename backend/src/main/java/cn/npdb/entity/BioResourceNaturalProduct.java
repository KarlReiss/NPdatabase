package cn.npdb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@TableName("bio_resource_natural_products")
public class BioResourceNaturalProduct {
    @TableId(type = IdType.AUTO)
    private Long id;

    private Long bioResourceId;
    private Long naturalProductId;

    private BigDecimal contentValue;
    private String contentUnit;
    private String contentPart;

    private String isolationMethod;
    private String refId;
    private String refIdType;

    private LocalDateTime createdAt;
}
