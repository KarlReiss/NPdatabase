package cn.npdb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@TableName("prescription_resources")
public class PrescriptionResource {
    @TableId(type = IdType.AUTO)
    private Long id;

    private Long prescriptionId;
    private Long bioResourceId;

    private BigDecimal dosageValue;
    private String dosageUnit;
    private String dosageText;
    private String role;
    private String roleChinese;
    private String processingMethod;
    private String processingNote;
    private String componentId;
    private String barcode;
    private Integer sortOrder;

    private LocalDateTime createdAt;
}
