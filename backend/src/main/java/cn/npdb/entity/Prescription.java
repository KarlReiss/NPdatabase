package cn.npdb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@TableName("prescriptions")
public class Prescription {
    @TableId(type = IdType.AUTO)
    private Long id;

    private String prescriptionId;
    private String chineseName;
    private String pinyinName;
    private String englishName;
    private String alias;

    private String sourceBook;
    private String sourceDynasty;
    private String sourceAuthor;

    private String category;
    private String subcategory;

    private String functions;
    private String indications;
    private String indicationsModern;
    private String syndrome;

    private String compositionText;
    private String dosageForm;
    private String preparationMethod;
    private String usageMethod;
    private String dosage;

    private String contraindications;
    private String precautions;
    private String adverseReactions;

    private String pharmacology;
    private String clinicalApplication;

    private String targetTissues;
    private String relatedDiseases;

    private String tcmidId;
    private String tcmspId;
    private String symmapId;
    private String diseaseIcd11Category;
    private String humanTissues;
    private String reference;
    private String referenceBook;

    private String pharmacopoeiaRef;
    private String literatureRef;

    private Integer numOfHerbs;
    private Integer numOfNaturalProducts;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
