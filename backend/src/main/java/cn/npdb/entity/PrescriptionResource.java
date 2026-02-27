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

    private LocalDateTime createdAt;

    private String tcmidComponentId;
}
