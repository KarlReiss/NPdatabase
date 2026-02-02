package cn.npdb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@TableName("bio_resource_disease_associations")
public class BioResourceDiseaseAssociation {
    @TableId(type = IdType.AUTO)
    private Long id;

    private Long bioResourceId;
    private Long diseaseId;

    private String evidenceTherapeuticTarget;
    private Boolean evidenceTranscriptome;
    private String evidenceClinicalTrialPlant;
    private String evidenceClinicalTrialIngredient;
    private BigDecimal confidenceScore;
    private String source;
    private String sourceVersion;

    private LocalDateTime createdAt;
}
