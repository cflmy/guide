// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
    
    // 添加项目卡片的悬停效果
    const items = document.querySelectorAll('.item');
    items.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px) scale(1.02)';
            this.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.1)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(-3px) scale(1)';
            this.style.boxShadow = 'none';
        });
    });
    
    // 分类标题点击折叠/展开功能
    const categoryHeaders = document.querySelectorAll('.category h2');
    categoryHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const category = this.closest('.category');
            const itemsContainer = category.querySelector('.items');
            const isExpanded = !category.classList.contains('collapsed');
            
            if (isExpanded) {
                category.classList.add('collapsed');
                itemsContainer.style.maxHeight = '0';
                itemsContainer.style.opacity = '0';
            } else {
                category.classList.remove('collapsed');
                itemsContainer.style.maxHeight = itemsContainer.scrollHeight + 'px';
                itemsContainer.style.opacity = '1';
            }
        });
    });
    
    // 初始化样式
    document.querySelectorAll('.items').forEach(container => {
        container.style.maxHeight = container.scrollHeight + 'px';
        container.style.transition = 'max-height 0.3s ease, opacity 0.3s ease';
    });
    
    // 添加页面加载动画
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease';
        document.body.style.opacity = '1';
    }, 100);
    
    // 为链接添加复制功能
    const links = document.querySelectorAll('.link');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const text = this.textContent;
            navigator.clipboard.writeText(text).then(() => {
                const originalText = this.textContent;
                this.textContent = '已复制!';
                this.style.color = '#28a745';
                setTimeout(() => {
                    this.textContent = originalText;
                    this.style.color = '#3498db';
                }, 2000);
            });
        });
    });
    
    // 响应式调整
    function handleResize() {
        const isMobile = window.innerWidth < 768;
        const itemsContainers = document.querySelectorAll('.items');
        
        if (!isMobile) {
            // 大屏幕时确保所有内容都展开
            document.querySelectorAll('.category').forEach(category => {
                category.classList.remove('collapsed');
            });
            
            itemsContainers.forEach(container => {
                container.style.maxHeight = 'none';
                container.style.opacity = '1';
            });
        }
    }
    
    // 初始调用
    handleResize();
    
    // 监听窗口大小变化
    window.addEventListener('resize', handleResize);
});