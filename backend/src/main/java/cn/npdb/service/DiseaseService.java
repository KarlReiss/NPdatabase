package cn.npdb.service;

import cn.npdb.entity.Disease;
import com.baomidou.mybatisplus.extension.service.IService;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;

import java.util.List;

public interface DiseaseService extends IService<Disease> {
    Page<Disease> listPage(long page, long pageSize, String q, String category);

    List<String> listCategories();
}
