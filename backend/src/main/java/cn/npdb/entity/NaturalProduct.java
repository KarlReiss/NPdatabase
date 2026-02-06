package cn.npdb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@TableName("natural_products")
public class NaturalProduct {
    @TableId(type = IdType.AUTO)
    private Long id;

    private String npId;
    private String inchikey;

    private String prefName;
    private String iupacName;
    private String nameInitial;

    private String inchi;
    private String smiles;

    private String chemblId;
    private String pubchemId;

    private BigDecimal molecularWeight;
    private BigDecimal xlogp;
    private BigDecimal psa;
    private String formula;
    private Integer hBondDonors;
    private Integer hBondAcceptors;
    private Integer rotatableBonds;

    // 新增理化性质字段
    private BigDecimal logS;
    private BigDecimal logD;
    private BigDecimal logP;
    private BigDecimal tpsa;
    private Integer ringCount;

    private Integer numOfOrganism;
    private Integer numOfTarget;
    private Integer numOfActivity;

    private Boolean ifQuantity;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
