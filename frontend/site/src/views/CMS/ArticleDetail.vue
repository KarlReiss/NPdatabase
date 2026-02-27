<template>
  <div class="max-w-[1440px] mx-auto px-6 py-6">
    <nav
      class="text-xs text-slate-500 mb-5 flex items-center space-x-2 bg-[#f1f1f1] dark:bg-[var(--el-bg-color)] p-4 rounded-1"
    >
      <RouterLink
        to="/"
        class="color-[#212121] dark:color-white hover:color-[var(--el-color-primary)] select-none no-underline hover:no-underline"
        >首页</RouterLink
      >
      <span class="dark:color-white">></span>
      <span class="text-slate-700 font-medium select-none">{{ article.name }}</span>
    </nav>

    <section
      class="bg-white rounded-md border dark:bg-[var(--el-bg-color)] border-[#E2E8F0] shadow-sm p-6 min-h-[220px] mb-6"
    >
      <div v-html="article.content"> </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { computed } from 'vue'
const route = useRoute()

const articleList = computed(() => {
  return [
    {
      id: 'user-guide',
      name: '使用指南',
      content: `<!-- 数据库指南 -->
                <div v-if="activeTab === 'guide'" class="tab-content">
                    <h2 class="content-title" style="color: #20558A; font-size: 1.8rem; margin-bottom: 25px; padding-bottom: 15px; border-bottom: 2px solid #e6f2ff; display: flex; align-items: center;">
                        <i class="fas fa-book-open content-icon" style="margin-right: 12px; font-size: 1.6rem;"></i>
                        数据库指南
                    </h2>
                    <div class="content-body" style="font-size: 1.05rem; line-height: 1.8;">
                        <p style="margin-bottom: 16px; color: #444;">欢迎使用云南天然产物活性数据库。本数据库致力于收集、整理和分析云南地区丰富的天然产物资源及其生物活性数据，为药物发现、功能食品开发和科学研究提供数据支持。</p>
                        
                        <div class="highlight" style="background-color: #e6f2ff; padding: 20px; border-radius: 8px; border-left: 4px solid #20558A; margin: 20px 0;">
                            <p style="margin-bottom: 16px; color: #444;"><strong>核心目标：</strong>构建云南天然产物资源的数字化平台，揭示其活性成分与作用机制，促进天然产物的合理开发利用。</p>
                        </div>
                        
                        <div class="compound-stats" style="display: flex; flex-wrap: wrap; gap: 20px; margin: 25px 0;">
                            <div class="stat-card" style="flex: 1; min-width: 200px; background: #e6f2ff; padding: 20px; border-radius: 8px; text-align: center; border: 1px solid #c8e6c9;">
                                <div class="stat-number" style="font-size: 2.2rem; font-weight: 700; color: #20558A; margin-bottom: 8px;">8,500+</div>
                                <div class="stat-label" style="color: #20558A; font-size: 1rem;">天然产物化合物</div>
                            </div>
                            <div class="stat-card" style="flex: 1; min-width: 200px; background: #e6f2ff; padding: 20px; border-radius: 8px; text-align: center; border: 1px solid #c8e6c9;">
                                <div class="stat-number" style="font-size: 2.2rem; font-weight: 700; color: #20558A; margin-bottom: 8px;">2,300+</div>
                                <div class="stat-label" style="color: #20558A; font-size: 1rem;">药用植物物种</div>
                            </div>
                            <div class="stat-card" style="flex: 1; min-width: 200px; background: #e6f2ff; padding: 20px; border-radius: 8px; text-align: center; border: 1px solid #c8e6c9;">
                                <div class="stat-number" style="font-size: 2.2rem; font-weight: 700; color: #20558A; margin-bottom: 8px;">15,000+</div>
                                <div class="stat-label" style="color: #20558A; font-size: 1rem;">活性测试数据</div>
                            </div>
                        </div>
                        
                        <h3 style="color: #20558A; margin: 25px 0 12px; font-size: 1.4rem;">主要功能模块</h3>
                        <ol style="padding-left: 20px; margin-bottom: 20px;">
                            <li style="margin-bottom: 10px;"><strong>化合物检索：</strong>按名称、分子式、结构相似性等查询天然产物化合物信息。</li>
                            <li style="margin-bottom: 10px;"><strong>物种查询：</strong>检索云南特有药用植物的化学成分与活性数据。</li>
                            <li style="margin-bottom: 10px;"><strong>活性筛选：</strong>根据抗肿瘤、抗菌、抗炎等活性类型筛选化合物。</li>
                            <li style="margin-bottom: 10px;"><strong>结构分析：</strong>提供化合物结构可视化、理化性质计算等功能。</li>
                            <li style="margin-bottom: 10px;"><strong>数据挖掘：</strong>开展构效关系、作用机制等分析研究。</li>
                        </ol>
                        
                        <h3 style="color: #20558A; margin: 25px 0 12px; font-size: 1.4rem;">使用方式</h3>
                        <ul style="padding-left: 20px; margin-bottom: 20px;">
                            <li style="margin-bottom: 10px;"><strong>快速检索：</strong>通过关键词搜索化合物、物种或活性信息。</li>
                            <li style="margin-bottom: 10px;"><strong>高级筛选：</strong>使用多条件组合筛选，精确查找目标数据。</li>
                            <li style="margin-bottom: 10px;"><strong>批量下载：</strong>支持化合物结构、活性数据批量导出。</li>
                            <li style="margin-bottom: 10px;"><strong>个性化服务：</strong>注册用户可保存检索历史、创建个人收藏夹。</li>
                        </ul>
                        
                        <h3 style="color: #20558A; margin: 25px 0 12px; font-size: 1.4rem;">注意事项</h3>
                        <p style="margin-bottom: 16px; color: #444;">1. 本数据库数据主要来源于公开发表的科学文献和实验研究，仅供参考。</p>
                        <p style="margin-bottom: 16px; color: #444;">2. 数据定期更新，建议关注最新版本。</p>
                        <p style="margin-bottom: 16px; color: #444;">3. 使用数据发表研究成果时，请引用原始文献和本数据库。</p>
                        <p style="margin-bottom: 16px; color: #444;">4. 商业用途请联系我们获取授权。</p>
                    </div>
                </div>`
    },
    {
      id: 'data-source',
      name: '数据来源',
      content: `<!-- 数据来源 -->
                <div v-if="activeTab === 'source'" class="tab-content">
                    <h2 class="content-title" style="color: #20558A; font-size: 1.8rem; margin-bottom: 25px; padding-bottom: 15px; border-bottom: 2px solid #e6f2ff; display: flex; align-items: center;">
                        <i class="fas fa-database content-icon" style="margin-right: 12px; font-size: 1.6rem;"></i>
                        数据来源
                    </h2>
                    <div class="content-body" style="font-size: 1.05rem; line-height: 1.8;">
                        <p style="margin-bottom: 16px; color: #444;">云南天然产物活性数据库的数据来源于多个权威渠道，涵盖云南丰富的生物资源和天然产物研究成果，确保数据的科学性、准确性和完整性。</p>
                        
                        <div class="region-map" style="width: 100%; height: 200px; background: linear-gradient(to right, #44c6e1, #0cadcf, #13adcd, #0994b1, #1878af, #1f71c5, #20558A); border-radius: 8px; margin: 20px 0; position: relative; overflow: hidden;">
                            <div class="region-label" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: white; font-size: 1.3rem; font-weight: bold; text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">云南 · 生物多样性热点地区</div>
                        </div>
                        
                        <div class="data-source-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-top: 20px;">
                            <div class="source-card" style="background: #e6f2ff; padding: 20px; border-radius: 8px; border-top: 4px solid #20558A; transition: transform 0.3s ease;">
                                <div class="source-title" style="color: #20558A; font-weight: 600; margin-bottom: 10px; font-size: 1.2rem;">科研文献与专利</div>
                                <p style="margin-bottom: 16px; color: #444;">收录来自PubMed、CNKI、Web of Science等数据库的科研文献，以及国内外相关专利中的天然产物活性数据。</p>
                            </div>
                            
                            <div class="source-card" style="background: #e6f2ff; padding: 20px; border-radius: 8px; border-top: 4px solid #20558A; transition: transform 0.3s ease;">
                                <div class="source-title" style="color: #20558A; font-weight: 600; margin-bottom: 10px; font-size: 1.2rem;">实地采集与鉴定</div>
                                <p style="margin-bottom: 16px; color: #444;">基于中国科学院昆明植物研究所、云南大学等机构的实地采集、标本鉴定和化学成分分析数据。</p>
                            </div>
                            
                            <div class="source-card" style="background: #e6f2ff; padding: 20px; border-radius: 8px; border-top: 4px solid #20558A; transition: transform 0.3s ease;">
                                <div class="source-title" style="color: #20558A; font-weight: 600; margin-bottom: 10px; font-size: 1.2rem;">合作研究项目</div>
                                <p style="margin-bottom: 16px; color: #444;">整合国家自然科学基金、云南省科技计划等项目产生的天然产物活性筛选和机制研究数据。</p>
                            </div>
                            
                            <div class="source-card" style="background: #e6f2ff; padding: 20px; border-radius: 8px; border-top: 4px solid #20558A; transition: transform 0.3s ease;">
                                <div class="source-title" style="color: #20558A; font-weight: 600; margin-bottom: 10px; font-size: 1.2rem;">公开数据库整合</div>
                                <p style="margin-bottom: 16px; color: #444;">关联PubChem、ChEMBL、TCMSP等国际知名数据库，实现数据交叉验证和补充。</p>
                            </div>
                        </div>
                        
                        <h3 style="color: #20558A; margin: 25px 0 12px; font-size: 1.4rem;">数据覆盖范围</h3>
                        <ul style="padding-left: 20px; margin-bottom: 20px;">
                            <li style="margin-bottom: 10px;"><strong>地理范围：</strong>主要覆盖云南省及周边地区，包括西双版纳、迪庆、大理等生物多样性热点区域。</li>
                            <li style="margin-bottom: 10px;"><strong>物种类型：</strong>涵盖药用植物、真菌、微生物等各类生物资源。</li>
                            <li style="margin-bottom: 10px;"><strong>化合物类别：</strong>包括生物碱、黄酮、萜类、甾体、多糖等主要天然产物类型。</li>
                            <li style="margin-bottom: 10px;"><strong>活性类型：</strong>抗肿瘤、抗菌、抗病毒、抗炎、抗氧化、神经保护等生物活性数据。</li>
                        </ul>
                        
                        <h3 style="color: #20558A; margin: 25px 0 12px; font-size: 1.4rem;">数据质量控制</h3>
                        <p style="margin-bottom: 16px; color: #444;">为确保数据质量，我们建立了严格的质量控制体系：</p>
                        <ul style="padding-left: 20px; margin-bottom: 20px;">
                            <li style="margin-bottom: 10px;"><strong>标准化处理：</strong>统一化合物命名、结构表示和活性数据单位。</li>
                            <li style="margin-bottom: 10px;"><strong>多级审核：</strong>数据采集、清洗、验证和专家评审四级质量控制流程。</li>
                            <li style="margin-bottom: 10px;"><strong>定期更新：</strong>每半年全面更新一次，重要数据实时补充。</li>
                            <li style="margin-bottom: 10px;"><strong>用户反馈：</strong>建立用户纠错和反馈机制，持续改进数据质量。</li>
                        </ul>
                    </div>
                </div>`
    },
    {
      id: 'regarding-project',
      name: '关于项目',
      content: `<!-- 关于项目 -->
                <div v-if="activeTab === 'about'" class="tab-content">
                    <h2 class="content-title" style="color: #20558A; font-size: 1.8rem; margin-bottom: 25px; padding-bottom: 15px; border-bottom: 2px solid #e6f2ff; display: flex; align-items: center;">
                        <i class="fas fa-info-circle content-icon" style="margin-right: 12px; font-size: 1.6rem;"></i>
                        关于项目
                    </h2>
                    <div class="content-body" style="font-size: 1.05rem; line-height: 1.8;">
                        <p style="margin-bottom: 16px; color: #444;">云南天然产物活性数据库是由云南省天然产物研究重点实验室牵头，联合多所高校和科研机构共同建设的专业数据库，旨在系统整理和挖掘云南特色天然产物资源。</p>
                        
                        <h3 style="color: #20558A; margin: 25px 0 12px; font-size: 1.4rem;">项目背景</h3>
                        <p style="margin-bottom: 16px; color: #444;">云南是中国生物多样性最丰富的省份，素有"植物王国"、"药物宝库"之称。为系统整理云南丰富的天然产物资源，促进其科学研究和合理利用。</p>
                        
                        <h3 style="color: #20558A; margin: 25px 0 12px; font-size: 1.4rem;">项目目标</h3>
                        <ul style="padding-left: 20px; margin-bottom: 20px;">
                            <li style="margin-bottom: 10px;"><strong>资源数字化：</strong>系统整理云南天然产物资源，建立数字化信息平台。</li>
                            <li style="margin-bottom: 10px;"><strong>数据标准化：</strong>制定天然产物数据标准，促进数据共享与交流。</li>
                            <li style="margin-bottom: 10px;"><strong>研究支撑：</strong>为新药研发、功能食品开发提供数据支持。</li>
                            <li style="margin-bottom: 10px;"><strong>知识传播：</strong>普及天然产物知识，促进生物资源可持续利用。</li>
                        </ul>
                        
                        <h3 style="color: #20558A; margin: 25px 0 12px; font-size: 1.4rem;">项目特色</h3>
                        <ol style="padding-left: 20px; margin-bottom: 20px;">
                            <li style="margin-bottom: 10px;"><strong>地域特色鲜明：</strong>专注于云南特有、特色天然产物资源。</li>
                            <li style="margin-bottom: 10px;"><strong>数据深度整合：</strong>整合化学结构、活性数据、作用机制等多维度信息。</li>
                            <li style="margin-bottom: 10px;"><strong>研究工具集成：</strong>提供虚拟筛选、分子对接、构效关系分析等研究工具。</li>
                            <li style="margin-bottom: 10px;"><strong>开放共享：</strong>遵循FAIR原则，促进数据开放和学术共享。</li>
                        </ol>
                        
                        <h3 style="color: #20558A; margin: 25px 0 12px; font-size: 1.4rem;">项目团队</h3>
                        <p style="margin-bottom: 16px; color: #444;">项目由云南省天然产物研究重点实验室主任张明教授领衔，联合中国科学院昆明植物研究所、云南大学、昆明医科大学等机构的专家团队共同建设。同时得到国家自然科学基金委员会和云南省科技厅的资助。</p>
                        
                        <h3 style="color: #20558A; margin: 25px 0 12px; font-size: 1.4rem;">合作网络</h3>
                        <p style="margin-bottom: 16px; color: #444;">我们与国内外多家研究机构建立了合作关系，包括：</p>
                        <ul style="padding-left: 20px; margin-bottom: 20px;">
                            <li style="margin-bottom: 10px;">中国科学院昆明植物研究所</li>
                            <li style="margin-bottom: 10px;">云南大学自然资源药物化学教育部重点实验室</li>
                            <li style="margin-bottom: 10px;">昆明医科大学天然药物药理重点实验室</li>
                            <li style="margin-bottom: 10px;">美国密西西比大学天然产物研究中心</li>
                            <li style="margin-bottom: 10px;">日本东京大学药学部</li>
                        </ul>
                        
                        <div class="highlight" style="background-color: #e6f2ff; padding: 20px; border-radius: 8px; border-left: 4px solid #20558A; margin: 20px 0;">
                            <p style="margin-bottom: 16px; color: #444;"><strong>项目成果：</strong>数据库上线以来，已收录8500+个天然产物化合物，2300+种药用植物，15000+条活性测试数据。累计服务科研人员超过10000人次，支持发表SCI论文200余篇。</p>
                        </div>
                    </div>
                </div>`
    },
    {
      id: 'contact-us',
      name: '联系我们',
      content: `<!-- 联系我们 -->
                <div v-if="activeTab === 'contact'" class="tab-content">
                    <h2 class="content-title" style="color: #20558A; font-size: 1.8rem; margin-bottom: 25px; padding-bottom: 15px; border-bottom: 2px solid #e6f2ff; display: flex; align-items: center;">
                        <i class="fas fa-envelope content-icon" style="margin-right: 12px; font-size: 1.6rem;"></i>
                        联系我们
                    </h2>
                    <div class="content-body" style="font-size: 1.05rem; line-height: 1.8;">
                        <p style="margin-bottom: 16px; color: #444;">感谢您对云南天然产物活性数据库的关注与支持。如果您有任何问题、建议或合作意向，欢迎通过以下方式与我们联系。</p>
                        
                        <div class="contact-item" style="display: flex; margin-bottom: 15px; padding: 12px; background: #e6f2ff; border-radius: 8px;">
                            <div class="contact-icon" style="color: #20558A; font-size: 1.3rem; width: 40px; text-align: center;">
                                <i class="fas fa-map-marker-alt"></i>
                            </div>
                            <div class="contact-info" style="flex: 1;">
                                <div class="contact-label" style="font-weight: 600; color: #20558A; margin-bottom: 3px;">地址</div>
                                <div>云南省昆明市XXXXXXXXXXXX 云南省天然产物研究重点实验室（邮编：650000）</div>
                            </div>
                        </div>
                        
                        <div class="contact-item" style="display: flex; margin-bottom: 15px; padding: 12px; background: #e6f2ff; border-radius: 8px;">
                            <div class="contact-icon" style="color: #20558A; font-size: 1.3rem; width: 40px; text-align: center;">
                                <i class="fas fa-phone"></i>
                            </div>
                            <div class="contact-info" style="flex: 1;">
                                <div class="contact-label" style="font-weight: 600; color: #20558A; margin-bottom: 3px;">电话</div>
                                <div>实验室办公室：0871-1234567（工作日 8:30-12:00, 14:00-17:30）</div>
                                <div>技术支持：0871-7654321（工作日 9:00-17:30）</div>
                            </div>
                        </div>
                        
                        <div class="contact-item" style="display: flex; margin-bottom: 15px; padding: 12px; background: #e6f2ff; border-radius: 8px;">
                            <div class="contact-icon" style="color: #20558A; font-size: 1.3rem; width: 40px; text-align: center;">
                                <i class="fas fa-envelope"></i>
                            </div>
                            <div class="contact-info" style="flex: 1;">
                                <div class="contact-label" style="font-weight: 600; color: #20558A; margin-bottom: 3px;">电子邮箱</div>
                                <div>数据库咨询：xxxxxx@ynu.edu.cn</div>
                                <div>技术支持：support@xxxxxx.org</div>
                                <div>数据提交：data@xxxxxx.org</div>
                                <div>合作交流：collaboration@xxxxxx.org</div>
                            </div>
                        </div>
                        
                        <div class="contact-item" style="display: flex; margin-bottom: 15px; padding: 12px; background: #e6f2ff; border-radius: 8px;">
                            <div class="contact-icon" style="color: #20558A; font-size: 1.3rem; width: 40px; text-align: center;">
                                <i class="fas fa-clock"></i>
                            </div>
                            <div class="contact-info" style="flex: 1;">
                                <div class="contact-label" style="font-weight: 600; color: #20558A; margin-bottom: 3px;">办公时间</div>
                                <div>周一至周五：8:30-12:00，14:00-17:30</div>
                                <div>周末及法定节假日休息</div>
                            </div>
                        </div>
                        
                        <h3 style="color: #20558A; margin: 25px 0 12px; font-size: 1.4rem;">数据提交与共享</h3>
                        <p style="margin-bottom: 16px; color: #444;">我们欢迎研究人员提交云南天然产物相关数据，共同完善数据库内容：</p>
                        <ul style="padding-left: 20px; margin-bottom: 20px;">
                            <li style="margin-bottom: 10px;"><strong>数据提交：</strong>请下载数据提交模板，按要求整理数据后发送至data@ynnpdb.org。</li>
                            <li style="margin-bottom: 10px;"><strong>数据引用：</strong>使用本数据库数据发表成果时，请引用：Zhang M, et al. Yunnan Natural Products Database, 2023.</li>
                            <li style="margin-bottom: 10px;"><strong>数据共享政策：</strong>本数据库遵循CC BY-NC 4.0协议，非商业用途可自由使用。</li>
                        </ul>
                        
                        <h3 style="color: #20558A; margin: 25px 0 12px; font-size: 1.4rem;">合作交流</h3>
                        <p style="margin-bottom: 16px; color: #444;">我们欢迎与国内外高校、科研院所、企业开展多种形式的合作：</p>
                        <ul style="padding-left: 20px; margin-bottom: 20px;">
                            <li style="margin-bottom: 10px;"><strong>学术合作：</strong>联合开展天然产物发现、活性评价与机制研究。</li>
                            <li style="margin-bottom: 10px;"><strong>技术合作：</strong>数据库开发、数据分析算法、人工智能应用等。</li>
                            <li style="margin-bottom: 10px;"><strong>产业合作：</strong>新药研发、功能食品开发、标准制定等。</li>
                        </ul>
                        
                        <div class="highlight" style="background-color: #e6f2ff; padding: 20px; border-radius: 8px; border-left: 4px solid #20558A; margin: 20px 0;">
                            <p style="margin-bottom: 16px; color: #444;"><strong>温馨提示：</strong>为确保问题得到及时处理，请在邮件主题中注明问题类型（咨询、技术、数据、合作等），并提供详细描述和必要附件。</p>
                        </div>
                    </div>
                </div>`
    }
  ]
})

const article = computed(() => {
  const id = String(route.params.id || '')
  return articleList.value.find((item) => item.id === id) ?? articleList.value[0]
})
</script>
