package cn.npdb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@TableName("bio_resources")
public class BioResource {
    @TableId(type = IdType.AUTO)
    private Long id;

    private String resourceId;
    private String resourceType;

    private String chineseName;
    private String officialChineseName;
    private String standardChineseName;
    private String latinName;

    private String taxonomyKingdom;
    private String taxonomyFamily;
    private String taxonomyGenus;
    private String taxonomySpecies;
    private String taxonomyId;
    private String speciesTaxId;
    private String genusTaxId;
    private String familyTaxId;
    private String cmaupId;

    private String tcmidId;

    private Integer numOfNaturalProducts;
    private Integer numOfPrescriptions;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
