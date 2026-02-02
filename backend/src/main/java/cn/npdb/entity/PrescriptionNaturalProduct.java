package cn.npdb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@TableName("prescription_natural_products")
public class PrescriptionNaturalProduct {
    @TableId(type = IdType.AUTO)
    private Long id;

    private Long prescriptionId;
    private Long naturalProductId;
    private Long sourceResourceId;

    private LocalDateTime createdAt;
}
