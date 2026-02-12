package cn.npdb.dto;

import lombok.Data;

import java.math.BigDecimal;

@Data
public class BioResourceNaturalProductItem {
    private String npId;
    private String prefName;
    private String iupacName;
    private BigDecimal molecularWeight;
    private BigDecimal xlogp;
    private BigDecimal psa;
    private String formula;

    private String orgIsolationPart;
    private String orgCollectLocation;
    private String orgCollectTime;
    private String refType;
    private String refId;
    private String refIdType;
    private String refUrl;
    private String newCpFound;
    private Integer sourceCount;
}
