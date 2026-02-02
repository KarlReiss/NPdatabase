package cn.npdb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

@Data
@TableName("v_prescription_detail")
public class PrescriptionDetailView {
    @TableId(type = IdType.AUTO)
    private Long id;

    private String prescriptionId;
    private String chineseName;
    private String category;
    private Integer numOfHerbs;
    private Integer numOfNaturalProducts;
    private Long herbCount;
    private Long directNaturalProductCount;
}
