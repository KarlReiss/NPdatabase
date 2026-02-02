package cn.npdb.service.impl;

import cn.npdb.entity.NaturalProduct;
import cn.npdb.mapper.NaturalProductMapper;
import cn.npdb.service.NaturalProductService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;

@Service
public class NaturalProductServiceImpl extends ServiceImpl<NaturalProductMapper, NaturalProduct> implements NaturalProductService {
}
