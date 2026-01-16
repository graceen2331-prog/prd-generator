import streamlit as st
import requests
import json
import re
import time

# ========== 全局样式配置 ==========
st.set_page_config(
    page_title="AI PRD Generator | 智能产品文档生成器",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
/* 全局样式 */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* 主容器 */
.main {
    padding: 0;
}

/* 顶部应用栏 */
.app-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem 2rem;
    border-radius: 0 0 20px 20px;
    color: white;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    margin-bottom: 2rem;
}

.header-title {
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0;
    background: linear-gradient(135deg, #ffffff 0%, #e2e8ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline-block;
}

.header-subtitle {
    font-size: 1rem;
    opacity: 0.9;
    margin-top: 0.5rem;
    color: rgba(255, 255, 255, 0.9);
}

/* 卡片样式 */
.custom-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    border: 1px solid #eef2f7;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
}

.custom-card:hover {
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    transform: translateY(-2px);
}

.card-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #2d3748;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* 输入框美化 */
.stTextInput>div>div>input, 
.stTextArea>div>div>textarea {
    border: 2px solid #e2e8f0;
    border-radius: 10px;
    padding: 0.8rem;
    font-size: 0.95rem;
    transition: all 0.3s;
}

.stTextInput>div>div>input:focus, 
.stTextArea>div>div>textarea:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    outline: none;
}

/* 按钮美化 */
.stButton>button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 0.8rem 1.5rem;
    border-radius: 10px;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    width: 100%;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.stButton>button:active {
    transform: translateY(0);
}

/* 侧边栏美化 */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a202c 0%, #2d3748 100%);
    padding-top: 2rem;
}

[data-testid="stSidebar"] .stSelectbox,
[data-testid="stSidebar"] .stTextInput,
[data-testid="stSidebar"] .stSlider {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    padding: 0.5rem;
}

[data-testid="stSidebar"] label {
    color: #e2e8f0 !important;
}

/* 标签页美化 */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: #f8fafc;
    padding: 8px;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 500;
    transition: all 0.3s;
}

.stTabs [data-baseweb="tab"]:hover {
    background-color: #edf2f7;
}

.stTabs [aria-selected="true"] {
    background-color: white !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    color: #667eea !important;
}

/* 指标卡片 */
.metric-card {
    background: linear-gradient(135deg, #f6f9ff 0%, #f0f4ff 100%);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    border-left: 4px solid #667eea;
}

.metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #2d3748;
    margin: 0.5rem 0;
}

.metric-label {
    font-size: 0.9rem;
    color: #718096;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* 加载动画 */
@keyframes pulse {
    0% { opacity: 0.6; }
    50% { opacity: 1; }
    100% { opacity: 0.6; }
}

.loading-pulse {
    animation: pulse 1.5s infinite;
}

/* 状态指示器 */
.status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 500;
}

.status-success {
    background: rgba(72, 187, 120, 0.1);
    color: #48bb78;
}

.status-warning {
    background: rgba(237, 137, 54, 0.1);
    color: #ed8936;
}

.status-error {
    background: rgba(245, 101, 101, 0.1);
    color: #f56565;
}

/* 分割线美化 */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
    margin: 2rem 0;
}

/* 代码块美化 */
.code-block {
    background: #1a202c;
    color: #e2e8f0;
    padding: 1rem;
    border-radius: 10px;
    font-family: 'Courier New', monospace;
    overflow-x: auto;
}

/* 提示框 */
.tooltip-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    background: #e2e8f0;
    color: #4a5568;
    border-radius: 50%;
    font-size: 0.8rem;
    margin-left: 0.5rem;
    cursor: help;
}
</style>
""", unsafe_allow_html=True)

# ========== 顶部应用栏 ==========
st.markdown("""
<div class="app-header">
    <div style="max-width: 1200px; margin: 0 auto;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <h1 class="header-title">🚀 AI PRD Generator</h1>
                <p class="header-subtitle">智能产品需求文档生成器 · 让创意快速落地</p>
            </div>
            <div style="display: flex; gap: 1rem; align-items: center;">
                <div class="status-indicator status-success" id="status-indicator">
                    <div style="width: 8px; height: 8px; background: #48bb78; border-radius: 50%;"></div>
                    系统就绪
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== 侧边栏配置 ==========
with st.sidebar:
    # 侧边栏标题
    st.markdown("<h2 style='color: white; margin-bottom: 2rem;'>⚙️ 配置中心</h2>", unsafe_allow_html=True)
    
    # API 配置卡片
    with st.container():
        st.markdown("### 🔑 API 设置")
        api_key = st.text_input("DeepSeek API Key", type="password", help="输入您的 DeepSeek API 密钥")
        api_base = st.text_input("API 地址", "https://api.deepseek.com/v1/chat/completions", 
                               help="DeepSeek API 接口地址")
    
    # 模型选择卡片
    with st.container():
        st.markdown("### 🧠 模型配置")
        model = st.selectbox(
            "选择AI模型",
            ["deepseek-chat", "deepseek-coder"],
            help="deepseek-chat: 通用对话模型 | deepseek-coder: 代码优化模型"
        )
    
    # 生成参数卡片
    with st.container():
        st.markdown("### 🎛️ 生成参数")
        col1, col2 = st.columns(2)
        with col1:
            temperature = st.slider("创造性", 0.0, 1.0, 0.7, 0.1, 
                                  help="值越高，生成内容越有创意；值越低，内容越稳定")
        with col2:
            max_tokens = st.number_input("最大长度", 100, 4000, 2000, 100,
                                       help="控制生成内容的长度")
    
    # 状态面板
    st.markdown("---")
    with st.container():
        st.markdown("### 📊 系统状态")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("API状态", "🟢 在线" if api_key else "🔴 离线")
        with col2:
            st.metric("生成次数", "0")
    
    # 帮助信息
    with st.expander("ℹ️ 使用帮助", expanded=False):
        st.markdown("""
        1. **获取API密钥**：访问 [DeepSeek官网](https://platform.deepseek.com/)
        2. **输入产品想法**：描述您的产品创意
        3. **调整参数**：根据需要调整生成参数
        4. **生成PRD**：点击生成按钮，等待AI创作
        5. **导出文档**：下载生成的PRD文档
        """)

# ========== 主内容区域 ==========
# 创建两列布局
col_left, col_right = st.columns([1.2, 0.8], gap="large")

with col_left:
    # 输入区域卡片
    with st.container():
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">💡 产品想法输入</div>', unsafe_allow_html=True)
        
        # 示例选择
        example_ideas = [
            "一个智能健身跟踪应用，能提供个性化训练计划",
            "团队协作工具，支持实时文档协作和项目管理",
            "个性化新闻推荐系统，基于兴趣和阅读习惯",
            "在线学习平台，提供互动式编程课程",
            "智能家居控制系统，支持语音和手机控制"
        ]
        
        selected_example = st.selectbox(
            "快速选择示例：",
            ["自定义输入"] + example_ideas,
            help="选择一个示例快速开始，或选择自定义输入"
        )
        
        # 产品想法输入
        if selected_example != "自定义输入":
            product_idea = st.text_area(
                "产品想法描述：",
                value=selected_example,
                height=150,
                placeholder="详细描述您的产品想法...",
                help="请尽可能详细地描述您的产品想法"
            )
        else:
            product_idea = st.text_area(
                "产品想法描述：",
                height=150,
                placeholder="例如：开发一个智能待办事项应用，能够根据任务优先级自动排序，并与日历同步...",
                help="请尽可能详细地描述您的产品想法"
            )
        
        # 额外要求
        with st.expander("📝 添加额外要求（可选）", expanded=False):
            additional_requirements = st.text_area(
                "其他需求或约束：",
                height=100,
                placeholder="例如：需要支持移动端、预算限制、时间要求、技术栈偏好等...",
                label_visibility="collapsed"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 生成按钮区域
    with st.container():
        col_btn1, col_btn2 = st.columns([3, 1])
        with col_btn1:
            generate_button = st.button(
                "🚀 生成 PRD 文档",
                type="primary",
                use_container_width=True,
                disabled=not (api_key and product_idea)
            )
        with col_btn2:
            if st.button("🔄 清空内容", use_container_width=True):
                st.rerun()
        
        # 提示信息
        if not api_key:
            st.warning("⚠️ 请先在侧边栏输入 API 密钥")
        elif not product_idea:
            st.info("💡 请输入产品想法描述")

with col_right:
    # 输出区域卡片
    with st.container():
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📄 PRD 输出结果</div>', unsafe_allow_html=True)
        
        if 'prd_content' not in st.session_state:
            st.session_state.prd_content = None
        if 'mermaid_code' not in st.session_state:
            st.session_state.mermaid_code = None
        
        if st.session_state.prd_content:
            # 创建标签页
            tab1, tab2, tab3 = st.tabs(["📋 完整文档", "📊 流程图", "💾 导出"])
            
            with tab1:
                st.markdown(st.session_state.prd_content)
            
            with tab2:
                if st.session_state.mermaid_code:
                    try:
                        from streamlit_mermaid import st_mermaid
                        st_mermaid(st.session_state.mermaid_code, height=400)
                    except ImportError:
                        st.warning("请安装 streamlit-mermaid 组件以渲染流程图")
                        st.code(st.session_state.mermaid_code, language="mermaid")
                else:
                    st.info("未生成流程图")
            
            with tab3:
                st.markdown("### 导出选项")
                
                col_exp1, col_exp2 = st.columns(2)
                with col_exp1:
                    st.download_button(
                        label="📥 下载 PRD",
                        data=st.session_state.prd_content,
                        file_name="prd_document.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                
                with col_exp2:
                    if st.session_state.mermaid_code:
                        st.download_button(
                            label="📥 下载流程图",
                            data=st.session_state.mermaid_code,
                            file_name="user_flow.mmd",
                            mime="text/plain",
                            use_container_width=True
                        )
                
                # 分享选项
                st.markdown("---")
                st.markdown("### 🔗 分享选项")
                st.code("https://prd-generator.example.com/share/12345", language="text")
                
        else:
            # 初始状态显示
            st.info("👈 在左侧输入产品想法并点击生成按钮")
            
            # 显示示例结构
            with st.expander("📖 查看 PRD 文档结构示例", expanded=False):
                st.markdown("""
                # 📋 产品需求文档（PRD）
                
                ## 🎯 产品概述
                - **产品愿景**：一句话描述产品目标
                - **目标用户**：核心用户群体
                - **核心价值**：解决的关键问题
                
                ## ⚙️ 功能需求
                ### 核心功能
                1. 功能一：详细描述
                2. 功能二：详细描述
                
                ### 辅助功能
                1. 功能一：详细描述
                
                ## 🔧 非功能需求
                - **性能**：响应时间要求
                - **安全**：数据保护措施
                - **可用性**：用户体验标准
                
                ## 📊 用户流程
                ```mermaid
                flowchart TD
                    A[开始] --> B[步骤一]
                    B --> C[步骤二]
                ```
                """)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ========== 底部状态栏 ==========
st.markdown("---")
with st.container():
    col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
    with col_stats1:
        st.markdown('<div class="metric-card"><div class="metric-label">生成时间</div><div class="metric-value">15s</div></div>', unsafe_allow_html=True)
    with col_stats2:
        st.markdown('<div class="metric-card"><div class="metric-label">文档长度</div><div class="metric-value">2.5K字</div></div>', unsafe_allow_html=True)
    with col_stats3:
        st.markdown('<div class="metric-card"><div class="metric-label">功能点</div><div class="metric-value">12个</div></div>', unsafe_allow_html=True)
    with col_stats4:
        st.markdown('<div class="metric-card"><div class="metric-label">流程图</div><div class="metric-value">已生成</div></div>', unsafe_allow_html=True)

# ========== 函数定义 ==========
def extract_mermaid_code(content):
    """从文本中提取Mermaid代码块"""
    pattern = r'```mermaid\s*(.*?)\s*```'
    matches = re.findall(pattern, content, re.DOTALL)
    return matches[0] if matches else None

def call_deepseek_api(api_key, api_base, model, prompt, temperature, max_tokens):
    """调用DeepSeek API"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "你是一个专业的产品经理，擅长编写详细、结构化的产品需求文档。请使用专业、清晰的语言。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        response = requests.post(api_base, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        st.error(f"API调用错误: {e}")
        return None
    except KeyError as e:
        st.error(f"API响应格式错误: {e}")
        return None

# ========== PRD 提示词模板 ==========
PRD_PROMPT_TEMPLATE = """请根据以下产品想法，生成一个专业、详细的产品需求文档（PRD）。

## 产品想法
{product_idea}
{additional_requirements}

## 文档要求
请按照以下结构生成Markdown格式的PRD文档：

# 📋 产品需求文档（PRD）

## 🎯 1. 产品概述
### 1.1 产品愿景
### 1.2 问题陈述
### 1.3 目标用户画像
### 1.4 核心价值主张
### 1.5 成功指标

## ⚙️ 2. 功能需求
### 2.1 核心功能（MVP）
（列出5-7个核心功能，每个功能包含：功能名称、详细描述、用户价值、优先级）

### 2.2 进阶功能
（列出3-5个未来规划功能）

### 2.3 功能优先级矩阵
（使用P0/P1/P2优先级标注）

## 🔧 3. 非功能需求
### 3.1 性能需求
- 响应时间要求
- 并发用户数
- 数据量规模

### 3.2 安全需求
- 数据加密
- 用户认证
- 隐私保护

### 3.3 可用性需求
- 用户体验标准
- 无障碍设计
- 多端适配

### 3.4 兼容性需求
- 浏览器/操作系统支持
- 设备适配
- API兼容性

## 📊 4. 用户流程与交互
### 4.1 主要用户旅程
### 4.2 关键交互流程

请生成一个Mermaid格式的流程图，描述主要用户流程。要求：
1. 使用专业的企业级流程图语法
2. 包含至少8个主要步骤
3. 包含决策分支
4. 使用合适的样式和布局

将流程图代码放在单独的mermaid代码块中。

## 🗺️ 5. 产品路线图
### 5.1 阶段一：MVP（1-3个月）
### 5.2 阶段二：功能扩展（3-6个月）
### 5.3 阶段三：生态建设（6-12个月）

## 📈 6. 衡量与优化
### 6.1 关键指标（KPIs）
### 6.2 数据分析需求
### 6.3 A/B测试计划

请确保文档：
- 专业、详细、实用
- 使用清晰的结构和标题
- 包含具体的数字和指标
- 适合团队协作和技术实现"""

# ========== 处理生成请求 ==========
if generate_button:
    if not product_idea:
        st.error("请输入产品想法！")
    elif not api_key:
        st.error("请输入DeepSeek API密钥！")
    else:
        # 显示加载状态
        with st.spinner("🤖 AI正在创作中，请稍候..."):
            progress_bar = st.progress(0)
            
            # 模拟进度
            for i in range(5):
                time.sleep(0.3)
                progress_bar.progress((i + 1) * 20)
            
            # 构建提示词
            prompt = PRD_PROMPT_TEMPLATE.format(
                product_idea=product_idea,
                additional_requirements=f"\n\n## 额外要求\n{additional_requirements}" if additional_requirements else ""
            )
            
            # 调用API
            prd_content = call_deepseek_api(
                api_key, api_base, model, 
                prompt, temperature, max_tokens
            )
            
            if prd_content:
                # 提取Mermaid代码
                mermaid_code = extract_mermaid_code(prd_content)
                
                # 清理PRD内容
                cleaned_prd = re.sub(r'```mermaid\s*.*?\s*```', '', prd_content, flags=re.DOTALL)
                
                # 保存到session state
                st.session_state.prd_content = cleaned_prd
                st.session_state.mermaid_code = mermaid_code
                
                # 完成进度
                progress_bar.progress(100)
                time.sleep(0.5)
                progress_bar.empty()
                
                # 显示成功消息
                st.success("✅ PRD生成成功！")
                st.balloons()
                
                # 刷新页面显示结果
                st.rerun()
            else:
                st.error("生成失败，请检查API配置或网络连接")

# ========== 底部信息 ==========
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #718096; font-size: 0.9rem; padding: 1rem;">
    <p>🚀 AI PRD Generator v1.0 · 使用 DeepSeek AI 技术驱动 · 生成内容仅供参考</p>
    <p style="margin-top: 0.5rem;">
        遇到问题？查看 
        <a href="#" style="color: #667eea; text-decoration: none;">使用文档</a> · 
        <a href="#" style="color: #667eea; text-decoration: none;">API参考</a> · 
        <a href="#" style="color: #667eea; text-decoration: none;">报告问题</a>
    </p>
</div>
""", unsafe_allow_html=True)