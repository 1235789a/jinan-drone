<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>济南天空广告 - 专业无人机视频拍摄</title>
    <style>
        :root {
            --primary: #3498db;
            --secondary: #2ecc71;
            --accent: #e74c3c;
            --dark: #2c3e50;
            --light: #ecf0f1;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Microsoft YaHei', sans-serif;
        }
        
        body {
            background-color: #f9f9f9;
            color: #333;
            line-height: 1.6;
            scroll-behavior: smooth;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        /* 导航栏 */
        header {
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
        }
        
        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 0;
        }
        
        .logo {
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--primary);
        }
        
        .nav-links {
            display: flex;
            list-style: none;
        }
        
        .nav-links li {
            margin-left: 25px;
        }
        
        .nav-links a {
            text-decoration: none;
            color: var(--dark);
            font-weight: 500;
            transition: color 0.3s;
        }
        
        .nav-links a:hover {
            color: var(--primary);
        }
        
        .admin-btn {
            background: var(--accent);
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.8rem;
            margin-left: 15px;
        }
        
        /* 英雄区域 */
        .hero {
            background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1506941433945-99a2aa4bd50a?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80');
            background-size: cover;
            background-position: center;
            color: white;
            padding: 150px 0 100px;
            text-align: center;
        }
        
        .hero h1 {
            font-size: 2.8rem;
            margin-bottom: 20px;
        }
        
        .hero p {
            font-size: 1.2rem;
            max-width: 700px;
            margin: 0 auto 30px;
        }
        
        .location-badge {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9rem;
            margin-bottom: 20px;
        }
        
        .cta-button {
            display: inline-block;
            background: var(--secondary);
            color: white;
            padding: 12px 30px;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
            font-size: 1.1rem;
            transition: background 0.3s, transform 0.3s;
            cursor: pointer;
            border: none;
        }
        
        .cta-button:hover {
            background: #27ae60;
            transform: translateY(-3px);
        }
        
        /* 服务介绍 */
        .services {
            padding: 80px 0;
            background: white;
        }
        
        .section-title {
            text-align: center;
            margin-bottom: 50px;
        }
        
        .section-title h2 {
            font-size: 2.2rem;
            color: var(--dark);
            margin-bottom: 15px;
        }
        
        .section-title p {
            color: #777;
            max-width: 700px;
            margin: 0 auto;
        }
        
        .service-cards {
            display: flex;
            justify-content: center;
            gap: 30px;
        }
        
        .service-card {
            background: var(--light);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            transition: transform 0.3s;
            cursor: pointer;
            max-width: 500px;
            width: 100%;
        }
        
        .service-card:hover {
            transform: translateY(-10px);
        }
        
        .service-img {
            height: 200px;
            background-color: var(--primary);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 3rem;
        }
        
        .service-content {
            padding: 25px;
        }
        
        .service-content h3 {
            font-size: 1.4rem;
            margin-bottom: 15px;
            color: var(--dark);
        }
        
        /* 价格套餐 */
        .pricing {
            padding: 80px 0;
            background: #f5f7fa;
        }
        
        .pricing-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }
        
        .pricing-card {
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s;
            border: 1px solid #eee;
            cursor: pointer;
        }
        
        .pricing-card:hover {
            transform: translateY(-10px);
        }
        
        .pricing-card.popular {
            transform: scale(1.05);
            border: 2px solid var(--primary);
        }
        
        .pricing-card.popular:hover {
            transform: scale(1.05) translateY(-10px);
        }
        
        .pricing-header {
            background: var(--primary);
            color: white;
            padding: 25px;
        }
        
        .pricing-card.popular .pricing-header {
            background: var(--secondary);
        }
        
        .pricing-header h3 {
            font-size: 1.5rem;
            margin-bottom: 10px;
        }
        
        .price {
            font-size: 2.5rem;
            font-weight: bold;
        }
        
        .pricing-body {
            padding: 25px;
        }
        
        .pricing-features {
            list-style: none;
            margin-bottom: 25px;
        }
        
        .pricing-features li {
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }
        
        .resolution-badge {
            display: inline-block;
            background: var(--primary);
            color: white;
            padding: 3px 10px;
            border-radius: 4px;
            font-size: 0.8rem;
            margin-left: 5px;
        }
        
        /* 媒体展示区域 */
        .media-showcase {
            padding: 80px 0;
            background: white;
        }
        
        .media-container {
            display: flex;
            flex-direction: column;
            gap: 40px;
        }
        
        /* 视频展示区 */
        .video-section, .photo-section {
            background: var(--light);
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        }
        
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
        }
        
        .section-header h3 {
            font-size: 1.5rem;
            color: var(--dark);
        }
        
        .upload-btn {
            background: var(--primary);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: background 0.3s;
        }
        
        .upload-btn:hover {
            background: #2980b9;
        }
        
        .upload-btn.disabled {
            background: #95a5a6;
            cursor: not-allowed;
        }
        
        .video-container {
            position: relative;
            width: 100%;
            max-width: 800px;
            margin: 0 auto;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        
        .video-player {
            width: 100%;
            display: block;
            background: #000;
        }
        
        .video-placeholder, .photo-placeholder {
            width: 100%;
            height: 400px;
            background: #ddd;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #777;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        .video-placeholder:hover, .photo-placeholder:hover {
            background: #ccc;
        }
        
        .placeholder-icon {
            font-size: 3rem;
            margin-bottom: 15px;
        }
        
        /* 照片展示区 */
        .photo-gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
        }
        
        .photo-item {
            position: relative;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 5px 10px rgba(0,0,0,0.1);
            aspect-ratio: 4/3;
            background: #eee;
            cursor: pointer;
        }
        
        .photo-item img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s;
        }
        
        .photo-item:hover img {
            transform: scale(1.05);
        }
        
        .photo-upload-area {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: #f5f5f5;
            border: 2px dashed #ccc;
            color: #777;
            transition: all 0.3s;
        }
        
        .photo-upload-area:hover {
            background: #eaeaea;
            border-color: var(--primary);
        }
        
        /* 联系表单 */
        .contact {
            padding: 80px 0;
            background: #f5f7fa;
        }
        
        .contact-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 50px;
        }
        
        .contact-info h3 {
            font-size: 1.5rem;
            margin-bottom: 20px;
            color: var(--dark);
        }
        
        .contact-details {
            margin-bottom: 30px;
        }
        
        .contact-details p {
            margin-bottom: 10px;
            display: flex;
            align-items: center;
        }
        
        .contact-details i {
            margin-right: 10px;
            color: var(--primary);
        }
        
        .contact-form .form-group {
            margin-bottom: 20px;
        }
        
        .contact-form label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
        }
        
        .contact-form input,
        .contact-form textarea,
        .contact-form select {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1rem;
        }
        
        .contact-form textarea {
            height: 150px;
            resize: vertical;
        }
        
        /* 管理员验证模态框 */
        .admin-modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.7);
            z-index: 3000;
            align-items: center;
            justify-content: center;
        }
        
        .admin-modal-content {
            background: white;
            padding: 30px;
            border-radius: 10px;
            width: 90%;
            max-width: 400px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .admin-modal h3 {
            margin-bottom: 20px;
            color: var(--dark);
            text-align: center;
        }
        
        .admin-form {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .admin-form input {
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1rem;
        }
        
        .admin-form button {
            background: var(--primary);
            color: white;
            border: none;
            padding: 12px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
            transition: background 0.3s;
        }
        
        .admin-form button:hover {
            background: #2980b9;
        }
        
        .close-admin-modal {
            position: absolute;
            top: 15px;
            right: 15px;
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: #777;
        }
        
        /* 图片查看模态框 */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 2000;
            align-items: center;
            justify-content: center;
        }
        
        .modal-content {
            max-width: 90%;
            max-height: 90%;
            position: relative;
        }
        
        .modal-content img {
            max-width: 100%;
            max-height: 100%;
            display: block;
            margin: 0 auto;
            border-radius: 8px;
        }
        
        .close-modal {
            position: absolute;
            top: 15px;
            right: 15px;
            color: white;
            font-size: 2rem;
            cursor: pointer;
            background: rgba(0,0,0,0.5);
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* 页脚 */
        footer {
            background: var(--dark);
            color: white;
            padding: 50px 0 20px;
        }
        
        .footer-content {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }
        
        .footer-column h3 {
            font-size: 1.2rem;
            margin-bottom: 20px;
            position: relative;
            padding-bottom: 10px;
        }
        
        .footer-column h3::after {
            content: '';
            position: absolute;
            left: 0;
            bottom: 0;
            width: 40px;
            height: 2px;
            background: var(--primary);
        }
        
        .footer-links {
            list-style: none;
        }
        
        .footer-links li {
            margin-bottom: 10px;
        }
        
        .footer-links a {
            color: #bbb;
            text-decoration: none;
            transition: color 0.3s;
        }
        
        .footer-links a:hover {
            color: white;
        }
        
        .copyright {
            text-align: center;
            padding-top: 20px;
            border-top: 1px solid #444;
            color: #bbb;
            font-size: 0.9rem;
        }
        
        /* 响应式设计 */
        @media (max-width: 768px) {
            .nav-links {
                display: none;
            }
            
            .hero h1 {
                font-size: 2.2rem;
            }
            
            .contact-container {
                grid-template-columns: 1fr;
            }
            
            .service-cards {
                flex-direction: column;
                align-items: center;
            }
            
            .pricing-cards {
                grid-template-columns: 1fr;
            }
            
            .pricing-card.popular {
                transform: scale(1);
            }
            
            .pricing-card.popular:hover {
                transform: translateY(-10px);
            }
            
            .section-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 15px;
            }
            
            .photo-gallery {
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            }
        }
    </style>
</head>
<body>
    <!-- 导航栏 -->
    <header>
        <div class="container">
            <nav>
                <div class="logo">济南天空广告</div>
                <ul class="nav-links">
                    <li><a href="#services">服务介绍</a></li>
                    <li><a href="#pricing">价格套餐</a></li>
                    <li><a href="#media">作品展示</a></li>
                    <li><a href="#contact">立即咨询</a></li>
                </ul>
                <button class="admin-btn" id="adminLoginBtn">管理员登录</button>
            </nav>
        </div>
    </header>

    <!-- 英雄区域 -->
    <section class="hero">
        <div class="container">
            <div class="location-badge">🚁 服务范围：山东济南地区 | 服务时间：周末 6:00-21:00</div>
            <h1>济南本地无人机视频拍摄服务<br>专业画质，实惠价格</h1>
            <p>专为济南本地商家提供的高质量无人机视频拍摄服务，2.7K/4K超清画质，让您的店铺宣传更出彩</p>
            <button class="cta-button" id="heroConsultBtn">立即咨询</button>
        </div>
    </section>

    <!-- 服务介绍 -->
    <section class="services" id="services">
        <div class="container">
            <div class="section-title">
                <h2>我们的无人机视频拍摄服务</h2>
                <p>专业级画质，满足您的各类宣传需求</p>
            </div>
            <div class="service-cards">
                <div class="service-card" data-service="video">
                    <div class="service-img">🎥</div>
                    <div class="service-content">
                        <h3>专业航拍视频拍摄</h3>
                        <p>使用DJI Mini 3无人机，提供高质量航拍视频服务，捕捉您店铺的最佳视角。</p>
                        <p><strong>适用场景：</strong>店铺展示、产品宣传、活动记录、房产展示、景区宣传</p>
                        <p><strong>服务时间：</strong>周末 6:00-21:00</p>
                        <p><strong>交付格式：</strong>MP4高清视频文件，支持2.7K/4K分辨率</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- 价格套餐 -->
    <section class="pricing" id="pricing">
        <div class="container">
            <div class="section-title">
                <h2>价格套餐</h2>
                <p>专为济南商家定制的实惠价格，点击套餐查看详情并咨询</p>
            </div>
            <div class="pricing-cards">
                <div class="pricing-card" data-plan="basic">
                    <div class="pricing-header">
                        <h3>5分钟视频拍摄</h3>
                        <div class="price">¥30<span>/次</span></div>
                    </div>
                    <div class="pricing-body">
                        <ul class="pricing-features">
                            <li>5分钟高清航拍视频 <span class="resolution-badge">2.7K</span></li>
                            <li>基础剪辑与调色</li>
                            <li>包含3-5个不同角度镜头</li>
                            <li>2.7K超清分辨率输出</li>
                            <li>2个工作日内交付</li>
                            <li>周末 6:00-21:00 拍摄</li>
                        </ul>
                        <button class="cta-button plan-select-btn">选择此套餐</button>
                    </div>
                </div>
                <div class="pricing-card popular" data-plan="standard">
                    <div class="pricing-header">
                        <h3>10分钟视频拍摄</h3>
                        <div class="price">¥45<span>/次</span></div>
                    </div>
                    <div class="pricing-body">
                        <ul class="pricing-features">
                            <li>10分钟高清航拍视频 <span class="resolution-badge">4K</span></li>
                            <li>精细剪辑与专业调色</li>
                            <li>包含5-8个不同角度镜头</li>
                            <li>4K超高清分辨率输出</li>
                            <li>3个工作日内交付</li>
                            <li>周末 6:00-21:00 拍摄</li>
                        </ul>
                        <button class="cta-button plan-select-btn">选择此套餐</button>
                    </div>
                </div>
            </div>
            <div style="text-align: center; margin-top: 30px; color: #666; font-size: 0.9rem;">
                <p>💡 注：所有价格均为济南市区内服务价格，郊区及周边县市需额外协商交通费用</p>
                <p>📅 服务时间：周末 6:00-21:00（需提前预约）</p>
            </div>
        </div>
    </section>

    <!-- 媒体展示区域 -->
    <section class="media-showcase" id="media">
        <div class="container">
            <div class="section-title">
                <h2>济南本地作品展示</h2>
                <p>展示我们在济南为各类商家拍摄的航拍视频和照片</p>
            </div>
            
            <div class="media-container">
                <!-- 视频展示区 -->
                <div class="video-section">
                    <div class="section-header">
                        <h3>航拍视频展示</h3>
                        <button class="upload-btn disabled" id="uploadVideoBtn" disabled>更换视频</button>
                    </div>
                    
                    <div class="video-container">
                        <!-- 默认视频占位符 -->
                        <div class="video-placeholder" id="videoPlaceholder">
                            <div class="placeholder-icon">🎥</div>
                            <p>需要管理员权限才能上传视频</p>
                            <p class="small-text">请联系网站管理员</p>
                        </div>
                        
                        <!-- 视频播放器 -->
                        <video class="video-player" id="videoPlayer" controls style="display: none;">
                            您的浏览器不支持视频播放
                        </video>
                    </div>
                    
                    <input type="file" id="videoUpload" accept="video/*" style="display: none;">
                </div>
                
                <!-- 照片展示区 -->
                <div class="photo-section">
                    <div class="section-header">
                        <h3>航拍照片展示</h3>
                        <button class="upload-btn disabled" id="uploadPhotoBtn" disabled>添加照片</button>
                    </div>
                    
                    <div class="photo-gallery" id="photoGallery">
                        <!-- 照片占位符 -->
                        <div class="photo-item photo-upload-area" id="photoUploadArea">
                            <div class="placeholder-icon">📷</div>
                            <p>需要管理员权限上传照片</p>
                        </div>
                    </div>
                    
                    <input type="file" id="photoUpload" accept="image/*" multiple style="display: none;">
                </div>
            </div>
        </div>
    </section>

    <!-- 联系表单 -->
    <section class="contact" id="contact">
        <div class="container">
            <div class="section-title">
                <h2>立即咨询</h2>
                <p>填写以下信息，我们将尽快与您联系（仅限济南地区，服务时间：周末 6:00-21:00）</p>
            </div>
            <div class="contact-container">
                <div class="contact-info">
                    <h3>联系我们</h3>
                    <div class="contact-details">
                        <p>📞 电话: 138****5678</p>
                        <p>✉️ 邮箱: contact@jnskyads.com</p>
                        <p>📍 服务区域: 山东济南全市</p>
                        <p>⏰ 服务时间: 周末 6:00-21:00</p>
                    </div>
                    <div class="business-info">
                        <h4>为什么选择我们？</h4>
                        <ul>
                            <li>济南本地服务，响应迅速</li>
                            <li>专业的DJI Mini 3无人机设备</li>
                            <li>2.7K/4K超高清画质</li>
                            <li>熟悉济南各区域飞行规定</li>
                            <li>实惠价格，高性价比</li>
                            <li>专业后期剪辑与调色</li>
                        </ul>
                    </div>
                </div>
                <div class="contact-form">
                    <form id="consultationForm">
                        <div class="form-group">
                            <label for="name">您的姓名 *</label>
                            <input type="text" id="name" required>
                        </div>
                        <div class="form-group">
                            <label for="phone">联系电话 *</label>
                            <input type="tel" id="phone" required>
                        </div>
                        <div class="form-group">
                            <label for="location">店铺所在区域 *</label>
                            <select id="location" required>
                                <option value="">请选择区域</option>
                                <option value="历下区">历下区</option>
                                <option value="市中区">市中区</option>
                                <option value="槐荫区">槐荫区</option>
                                <option value="天桥区">天桥区</option>
                                <option value="历城区">历城区</option>
                                <option value="长清区">长清区</option>
                                <option value="章丘区">章丘区</option>
                                <option value="济阳区">济阳区</option>
                                <option value="莱芜区">莱芜区</option>
                                <option value="钢城区">钢城区</option>
                                <option value="平阴县">平阴县</option>
                                <option value="商河县">商河县</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="business">店铺类型</label>
                            <input type="text" id="business" placeholder="例如：餐厅、零售店、培训机构等">
                        </div>
                        <div class="form-group">
                            <label for="plan">选择套餐 *</label>
                            <select id="plan" required>
                                <option value="">请选择套餐</option>
                                <option value="basic">5分钟视频拍摄 (2.7K) - ¥30</option>
                                <option value="standard">10分钟视频拍摄 (4K) - ¥45</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="preferred-time">期望拍摄时间</label>
                            <select id="preferred-time">
                                <option value="">请选择时间段</option>
                                <option value="周末上午">周末上午 (6:00-12:00)</option>
                                <option value="周末下午">周末下午 (12:00-18:00)</option>
                                <option value="周末晚上">周末晚上 (18:00-21:00)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="message">拍摄需求描述</label>
                            <textarea id="message" placeholder="请简要描述您的拍摄需求，例如拍摄内容、特殊角度要求等..."></textarea>
                        </div>
                        <button type="submit" class="cta-button">提交咨询</button>
                    </form>
                </div>
            </div>
        </div>
    </section>

    <!-- 管理员验证模态框 -->
    <div class="admin-modal" id="adminModal">
        <div class="admin-modal-content">
            <button class="close-admin-modal" id="closeAdminModal">&times;</button>
            <h3>管理员验证</h3>
            <form class="admin-form" id="adminForm">
                <input type="password" id="adminPassword" placeholder="请输入管理员密码" required>
                <button type="submit">验证身份</button>
            </form>
            <p id="adminMessage" style="margin-top: 15px; color: #e74c3c; text-align: center; display: none;">密码错误，请重试</p>
        </div>
    </div>

    <!-- 图片查看模态框 -->
    <div class="modal" id="imageModal">
        <div class="close-modal" id="closeModal">&times;</div>
        <div class="modal-content">
            <img id="modalImage" src="" alt="放大查看">
        </div>
    </div>

    <!-- 页脚 -->
    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-column">
                    <h3>济南天空广告</h3>
                    <p>专注于为济南本地企业提供专业的无人机视频拍摄服务，2.7K/4K超高清画质，实惠价格。</p>
                </div>
                <div class="footer-column">
                    <h3>快速链接</h3>
                    <ul class="footer-links">
                        <li><a href="#services">服务介绍</a></li>
                        <li><a href="#pricing">价格套餐</a></li>
                        <li><a href="#media">作品展示</a></li>
                        <li><a href="#contact">立即咨询</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>联系我们</h3>
                    <ul class="footer-links">
                        <li><a href="tel:13800005678">电话: 138****5678</a></li>
                        <li><a href="mailto:contact@jnskyads.com">邮箱: contact@jnskyads.com</a></li>
                        <li><a href="#">微信: JNSkyAds</a></li>
                    </ul>
                </div>
            </div>
            <div class="copyright">
                <p>&copy; 2024 济南天空广告无人机服务 - 服务范围：山东济南地区 | 服务时间：周末 6:00-21:00</p>
            </div>
        </div>
    </footer>

    <script>
        // 配置 - 在这里设置你的管理员密码
        const ADMIN_PASSWORD = "drone2024"; // 你可以修改这个密码
        
        // DOM元素
        const adminLoginBtn = document.getElementById('adminLoginBtn');
        const adminModal = document.getElementById('adminModal');
        const closeAdminModal = document.getElementById('closeAdminModal');
        const adminForm = document.getElementById('adminForm');
        const adminPassword = document.getElementById('adminPassword');
        const adminMessage = document.getElementById('adminMessage');
        
        const videoUpload = document.getElementById('videoUpload');
        const videoUploadBtn = document.getElementById('uploadVideoBtn');
        const videoPlaceholder = document.getElementById('videoPlaceholder');
        const videoPlayer = document.getElementById('videoPlayer');
        
        const photoUpload = document.getElementById('photoUpload');
        const photoUploadBtn = document.getElementById('uploadPhotoBtn');
        const photoUploadArea = document.getElementById('photoUploadArea');
        const photoGallery = document.getElementById('photoGallery');
        
        const imageModal = document.getElementById('imageModal');
        const modalImage = document.getElementById('modalImage');
        const closeModal = document.getElementById('closeModal');
        
        const heroConsultBtn = document.getElementById('heroConsultBtn');
        const serviceCards = document.querySelectorAll('.service-card');
        const pricingCards = document.querySelectorAll('.pricing-card');
        const planSelectBtns = document.querySelectorAll('.plan-select-btn');
        const consultationForm = document.getElementById('consultationForm');
        const planSelect = document.getElementById('plan');
        const locationSelect = document.getElementById('location');
        const preferredTimeSelect = document.getElementById('preferred-time');
        
        // 管理员登录状态
        let isAdmin = false;
        
        // 检查本地存储中的管理员状态
        function checkAdminStatus() {
            const adminStatus = localStorage.getItem('droneAdmin');
            if (adminStatus === 'true') {
                enableAdminFeatures();
            }
        }
        
        // 启用管理员功能
        function enableAdminFeatures() {
            isAdmin = true;
            videoUploadBtn.disabled = false;
            videoUploadBtn.classList.remove('disabled');
            photoUploadBtn.disabled = false;
            photoUploadBtn.classList.remove('disabled');
            videoPlaceholder.innerHTML = `
                <div class="placeholder-icon">🎥</div>
                <p>点击上传或拖放视频文件</p>
                <p class="small-text">支持 MP4, WebM, OGG 格式</p>
            `;
            photoUploadArea.innerHTML = `
                <div class="placeholder-icon">📷</div>
                <p>点击上传照片</p>
            `;
            
            // 保存管理员状态到本地存储
            localStorage.setItem('droneAdmin', 'true');
        }
        
        // 禁用管理员功能
        function disableAdminFeatures() {
            isAdmin = false;
            videoUploadBtn.disabled = true;
            videoUploadBtn.classList.add('disabled');
            photoUploadBtn.disabled = true;
            photoUploadBtn.classList.add('disabled');
            videoPlaceholder.innerHTML = `
                <div class="placeholder-icon">🎥</div>
                <p>需要管理员权限才能上传视频</p>
                <p class="small-text">请联系网站管理员</p>
            `;
            photoUploadArea.innerHTML = `
                <div class="placeholder-icon">📷</div>
                <p>需要管理员权限上传照片</p>
            `;
            
            // 移除管理员状态
            localStorage.removeItem('droneAdmin');
        }
        
        // 管理员登录按钮点击事件
        adminLoginBtn.addEventListener('click', () => {
            adminModal.style.display = 'flex';
        });
        
        // 关闭管理员模态框
        closeAdminModal.addEventListener('click', () => {
            adminModal.style.display = 'none';
            adminMessage.style.display = 'none';
            adminPassword.value = '';
        });
        
        // 管理员表单提交
        adminForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const password = adminPassword.value;
            
            if (password === ADMIN_PASSWORD) {
                enableAdminFeatures();
                adminModal.style.display = 'none';
                adminMessage.style.display = 'none';
                adminPassword.value = '';
                alert('管理员身份验证成功！您现在可以上传媒体文件。');
            } else {
                adminMessage.style.display = 'block';
                adminPassword.value = '';
            }
        });
        
        // 视频上传功能
        videoUploadBtn.addEventListener('click', () => {
            if (isAdmin) {
                videoUpload.click();
            }
        });
        
        videoPlaceholder.addEventListener('click', () => {
            if (isAdmin) {
                videoUpload.click();
            }
        });
        
        videoUpload.addEventListener('change', function(e) {
            if (!isAdmin) return;
            
            const file = e.target.files[0];
            if (file) {
                const videoURL = URL.createObjectURL(file);
                videoPlayer.src = videoURL;
                videoPlayer.style.display = 'block';
                videoPlaceholder.style.display = 'none';
                
                // 保存到本地存储
                try {
                    // 注意：对于大文件，localStorage可能不够用
                    // 这里我们只存储文件名作为示例
                    localStorage.setItem('droneVideo', file.name);
                } catch (error) {
                    console.error('保存视频信息失败:', error);
                }
            }
        });
        
        // 照片上传功能
        photoUploadBtn.addEventListener('click', () => {
            if (isAdmin) {
                photoUpload.click();
            }
        });
        
        photoUploadArea.addEventListener('click', () => {
            if (isAdmin) {
                photoUpload.click();
            }
        });
        
        photoUpload.addEventListener('change', function(e) {
            if (!isAdmin) return;
            
            const files = e.target.files;
            if (files.length > 0) {
                for (let i = 0; i < files.length; i++) {
                    addPhotoToGallery(files[i]);
                }
                
                // 保存照片信息到本地存储
                savePhotosToStorage();
            }
        });
        
        // 添加照片到画廊
        function addPhotoToGallery(file) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                const photoItem = document.createElement('div');
                photoItem.className = 'photo-item';
                
                const img = document.createElement('img');
                img.src = e.target.result;
                img.alt = '无人机航拍照片';
                
                // 点击查看大图
                img.addEventListener('click', function() {
                    modalImage.src = this.src;
                    imageModal.style.display = 'flex';
                });
                
                photoItem.appendChild(img);
                
                // 将新照片添加到上传区域之前
                photoGallery.insertBefore(photoItem, photoUploadArea);
            };
            
            reader.readAsDataURL(file);
        }
        
        // 保存照片到本地存储
        function savePhotosToStorage() {
            const photos = [];
            const photoItems = document.querySelectorAll('.photo-item:not(#photoUploadArea)');
            
            // 由于存储空间限制，我们只保存前10张照片
            photoItems.forEach((item, index) => {
                if (index < 10) {
                    const img = item.querySelector('img');
                    photos.push(img.src);
                }
            });
            
            try {
                localStorage.setItem('dronePhotos', JSON.stringify(photos));
            } catch (error) {
                console.error('保存照片失败:', error);
            }
        }
        
        // 从本地存储加载媒体
        function loadMediaFromStorage() {
            // 加载视频
            const savedVideo = localStorage.getItem('droneVideo');
            if (savedVideo) {
                // 注意：实际应用中，视频需要从服务器加载
                // 这里仅作演示
                videoPlayer.style.display = 'block';
                videoPlaceholder.style.display = 'none';
            }
            
            // 加载照片
            const savedPhotos = localStorage.getItem('dronePhotos');
            if (savedPhotos) {
                const photos = JSON.parse(savedPhotos);
                photos.forEach(photoSrc => {
                    const photoItem = document.createElement('div');
                    photoItem.className = 'photo-item';
                    
                    const img = document.createElement('img');
                    img.src = photoSrc;
                    img.alt = '无人机航拍照片';
                    
                    img.addEventListener('click', function() {
                        modalImage.src = this.src;
                        imageModal.style.display = 'flex';
                    });
                    
                    photoItem.appendChild(img);
                    photoGallery.insertBefore(photoItem, photoUploadArea);
                });
            }
        }
        
        // 关闭模态框
        closeModal.addEventListener('click', () => {
            imageModal.style.display = 'none';
        });
        
        imageModal.addEventListener('click', (e) => {
            if (e.target === imageModal) {
                imageModal.style.display = 'none';
            }
        });
        
        // 交互功能 - 服务介绍点击
        serviceCards.forEach(card => {
            card.addEventListener('click', function() {
                // 滚动到联系表单
                document.getElementById('contact').scrollIntoView({ behavior: 'smooth' });
                
                // 设置表单中的套餐类型
                setTimeout(() => {
                    document.getElementById('name').focus();
                }, 800);
                
                // 显示确认消息
                setTimeout(() => {
                    alert(`您已选择无人机视频拍摄服务，请填写联系方式，我们将尽快与您联系！`);
                }, 1000);
            });
        });
        
        // 交互功能 - 价格套餐点击
        pricingCards.forEach(card => {
            card.addEventListener('click', function() {
                const planType = this.getAttribute('data-plan');
                let planName = '';
                let planPrice = '';
                let resolution = '';
                
                switch(planType) {
                    case 'basic':
                        planName = '5分钟视频拍摄';
                        planPrice = '¥30';
                        resolution = '2.7K';
                        break;
                    case 'standard':
                        planName = '10分钟视频拍摄';
                        planPrice = '¥45';
                        resolution = '4K';
                        break;
                }
                
                // 滚动到联系表单
                document.getElementById('contact').scrollIntoView({ behavior: 'smooth' });
                
                // 设置表单中的套餐类型
                setTimeout(() => {
                    planSelect.value = planType;
                    document.getElementById('name').focus();
                }, 800);
                
                // 显示确认消息
                setTimeout(() => {
                    alert(`您已选择 "${planName} (${resolution}) - ${planPrice}"，请填写联系方式，我们将尽快与您联系！`);
                }, 1000);
            });
        });
        
        // 套餐选择按钮点击
        planSelectBtns.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.stopPropagation(); // 防止触发父元素的点击事件
                const card = this.closest('.pricing-card');
                const planType = card.getAttribute('data-plan');
                let planName = '';
                let planPrice = '';
                let resolution = '';
                
                switch(planType) {
                    case 'basic':
                        planName = '5分钟视频拍摄';
                        planPrice = '¥30';
                        resolution = '2.7K';
                        break;
                    case 'standard':
                        planName = '10分钟视频拍摄';
                        planPrice = '¥45';
                        resolution = '4K';
                        break;
                }
                
                // 滚动到联系表单
                document.getElementById('contact').scrollIntoView({ behavior: 'smooth' });
                
                // 设置表单中的套餐类型
                setTimeout(() => {
                    planSelect.value = planType;
                    document.getElementById('name').focus();
                }, 800);
                
                // 显示确认消息
                setTimeout(() => {
                    alert(`您已选择 "${planName} (${resolution}) - ${planPrice}"，请填写联系方式，我们将尽快与您联系！`);
                }, 1000);
            });
        });
        
        // 立即咨询按钮点击
        heroConsultBtn.addEventListener('click', function() {
            document.getElementById('contact').scrollIntoView({ behavior: 'smooth' });
            setTimeout(() => {
                document.getElementById('name').focus();
            }, 800);
        });
        
        // 表单提交
        consultationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const name = document.getElementById('name').value;
            const phone = document.getElementById('phone').value;
            const location = locationSelect.options[locationSelect.selectedIndex].text;
            const plan = planSelect.options[planSelect.selectedIndex].text;
            const preferredTime = preferredTimeSelect.options[preferredTimeSelect.selectedIndex].text;
            
            if (!location) {
                alert('请选择您所在的区域！');
                return;
            }
            
            if (!plan) {
                alert('请选择您感兴趣的套餐！');
                return;
            }
            
            let message = `感谢 ${name} 的咨询！\n\n您位于${location}，我们将在济南为您提供服务。\n\n您选择的套餐：${plan}\n`;
            
            if (preferredTime) {
                message += `期望拍摄时间：${preferredTime}\n`;
            }
            
            message += `\n我们将通过电话 ${phone} 与您联系，确认具体拍摄细节。\n\n我们将在24小时内与您联系！`;
            
            alert(message);
            
            this.reset();
        });
        
        // 页面加载时检查管理员状态并加载媒体
        window.addEventListener('DOMContentLoaded', () => {
            checkAdminStatus();
            loadMediaFromStorage();
        });
        
        // 平滑滚动
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const targetId = this.getAttribute('href');
                if(targetId === '#') return;
                
                const targetElement = document.querySelector(targetId);
                if(targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 80,
                        behavior: 'smooth'
                    });
                }
            });
        });
    </script>
</body>
</html>
