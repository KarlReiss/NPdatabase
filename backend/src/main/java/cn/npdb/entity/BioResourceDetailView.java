package cn.npdb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

@Data
@TableName("v_bio_resource_detail")
public class BioResourceDetailView {
    @TableId(type = IdType.AUTO)
    private Long id;

    private String resourceId;
    private String resourceType;
    private String chineseName;
    private String latinName;
    private String taxonomyFamily;
    private String taxonomyGenus;
    private Integer numOfNaturalProducts;
    private Integer numOfPrescriptions;
}
