// ========== 导航栏滚动阴影 ==========
window.addEventListener('scroll', function() {
  const navbar = document.querySelector('.navbar');
  if (window.scrollY > 10) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
});

// ========== 回到顶部按钮 ==========
(function() {
  const btn = document.createElement('div');
  btn.id = 'backToTop';
  btn.innerHTML = '↑';
  btn.title = '回到顶部';
  document.body.appendChild(btn);

  window.addEventListener('scroll', function() {
    if (window.scrollY > 300) {
      btn.classList.add('show');
    } else {
      btn.classList.remove('show');
    }
  });

  btn.addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
})();

// ========== 表单提交时按钮显示加载状态，防止重复提交 ==========
document.addEventListener('submit', function(e) {
  const form = e.target;
  const btn = form.querySelector('button[type="submit"]');
  if (btn && !btn.disabled) {
    // 可添加自定义加载提示，这里简单禁用按钮并改变文字
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>提交中...';
    // 提交后恢复（若表单验证失败可能不会触发，这里简单用定时器恢复，实际项目中应处理 ajax）
    setTimeout(function() {
      if (btn.disabled) {
        btn.disabled = false;
        btn.innerHTML = originalText;
      }
    }, 3000);
  }
});
