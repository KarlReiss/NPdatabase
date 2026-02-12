package cn.npdb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@TableName("bio_resource_natural_products")
public class BioResourceNaturalProduct {
    @TableId(type = IdType.AUTO)
    private Long id;

    private String orgId;
    private String npId;
    private String srcOrgRecordId;
    private String srcOrgPairId;
    private String srcOrgPair;
    private String newCpFound;
    private String orgIsolationPart;
    private String orgCollectLocation;
    private String orgCollectTime;
    private String refType;
    private String refId;
    private String refIdType;
    private String refUrl;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
