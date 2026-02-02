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
    private String latinName;
    private String englishName;
    private String pinyinName;
    private String alias;

    private String taxonomyKingdom;
    private String taxonomyPhylum;
    private String taxonomyClass;
    private String taxonomyOrder;
    private String taxonomyFamily;
    private String taxonomyGenus;
    private String taxonomySpecies;
    private String taxonomyId;
    private String speciesTaxId;
    private String genusTaxId;
    private String familyTaxId;
    private String cmaupId;

    private String medicinalPart;
    private String medicinalPartLatin;

    private String originRegion;
    private String distribution;
    private String habitat;

    private String tcmProperty;
    private String tcmFlavor;
    private String tcmMeridian;
    private String tcmToxicity;

    private String functions;
    private String indications;
    private String contraindications;

    private String mineralComposition;
    private String mineralCrystalSystem;
    private String mineralHardness;
    private String mineralColor;

    private String microbeStrain;
    private String microbeCultureCondition;
    private String microbeFermentationProduct;

    private String animalClass;
    private String animalConservationStatus;

    private String tcmidId;
    private String tcmspId;
    private String herbId;

    private String pharmacopoeiaRef;
    private String literatureRef;

    private String imageUrl;

    private Integer numOfNaturalProducts;
    private Integer numOfPrescriptions;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
