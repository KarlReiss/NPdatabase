package cn.npdb.dto;

import lombok.Data;

@Data
public class PrescriptionListItem {
    private String prescriptionId;
    private String chineseName;
    private String functions;
    private String diseaseIcd11Category;
    private Long bioResourceCount;
}
