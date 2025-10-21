<!doctype html>
<html lang="bn">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Barasat Kali Puja — Top Clubs</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root{
      --bg:#0f1724; /* slate-900 */
      --card:#0b1220;
      --muted:#9aa4b2;
      --accent1:#7c3aed; /* violet */
      --accent2:#06b6d4; /* cyan */
      --glass: rgba(255,255,255,0.05);
    }
    *{box-sizing:border-box}
    body{margin:0;font-family:Inter,system-ui,Segoe UI,Roboto,'Helvetica Neue',Arial;background:linear-gradient(180deg,var(--bg),#061021);color:#e6eef8;min-height:100vh}
    header{padding:28px 20px;display:flex;align-items:center;justify-content:space-between;gap:16px}
    .brand{display:flex;align-items:center;gap:12px}
    .logo{width:56px;height:56px;border-radius:12px;background:linear-gradient(135deg,var(--accent1),var(--accent2));display:flex;align-items:center;justify-content:center;font-weight:800;font-size:20px;box-shadow:0 6px 18px rgba(12,18,30,0.6)}
    h1{margin:0;font-size:20px}
    p.lead{margin:0;color:var(--muted);font-size:13px}
    main{padding:0 20px 60px}
    .searchbar{max-width:900px;margin:10px auto 18px;display:flex;gap:10px;align-items:center}
    .searchbar input{flex:1;padding:12px 14px;border-radius:10px;border:0;background:var(--card);color:inherit;outline: none;font-size:14px}
    .searchbar .btn{padding:10px 14px;border-radius:10px;border:0;background:linear-gradient(90deg,var(--accent1),var(--accent2));cursor:pointer;color:white;font-weight:600}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;max-width:1100px;margin:18px auto}
    .card{background:linear-gradient(180deg,rgba(255,255,255,0.02),var(--glass));padding:14px;border-radius:12px;border:1px solid rgba(255,255,255,0.04);backdrop-filter: blur(6px);}
    .card h3{margin:0 0 6px;font-size:16px}
    .addr{font-size:13px;color:var(--muted);margin-bottom:10px}
    .meta{display:flex;justify-content:space-between;align-items:center;gap:8px}
    .openmap{padding:8px 12px;border-radius:10px;border:0;background:transparent;color:var(--accent2);font-weight:700;cursor:pointer}
    .openmap:hover{transform:translateY(-1px)}
    .icon{display:inline-block;width:34px;height:34px;border-radius:8px;background:rgba(255,255,255,0.03);display:flex;align-items:center;justify-content:center}
    footer{max-width:1100px;margin:28px auto;color:var(--muted);font-size:13px;padding:20px}
    .hint{font-size:13px;color:var(--muted);margin-top:8px}
    @media (max-width:480px){header{padding:18px} .logo{width:48px;height:48px}}
  </style>
</head>
<body>
  <header>
    <div class="brand">
      <div class="logo">ব</div>
      <div>
        <h1>Barasat — Top Kali Puja Clubs</h1>
        <p class="lead">ক্লাবগুলোর তালিকা দেখুন — ক্লাবে ক্লিক করলে Google Maps এ ঠিকানাটি খুলবে।</p>
      </div>
    </div>
    <div style="text-align:right;min-width:220px">
      <div style="font-size:13px;color:var(--muted)">Location: Barasat, North 24 Parganas</div>
    </div>
  </header>

  <main>
    <div class="searchbar">
      <input id="search" placeholder="খুঁজুন: ক্লাবের নাম বা এলাকা..." />
      <button class="btn" id="clearBtn">Clear</button>
    </div>

    <section class="grid" id="list">
      <!-- Cards injected by JS -->
    </section>

    <footer>
      <div><strong>নোট:</strong> প্রতিটি ক্লাবের জন্য Google Maps খোলা হবে একটি নতুন ট্যাবে — অ্যাড্রেস/নাম সার্চের উপর ভিত্তি করে।</div>
      <div class="hint">আপনি চাইলে আমি ক্লাবগুলোর সঠিক ল্যাট/লং কোঅর্ডিনেট বসিয়ে দিতে পারি যাতে সরাসরি মার্কার দেখায়।</div>
    </footer>
  </main>

  <script>
    // Data: top 10 clubs + friendly address strings (used to open google maps search)
    const clubs = [
      {name:"Pioneer Athletic Club", addr:"Pioneer Park, Noapara, Barasat, West Bengal"},
      {name:"K.N.C. Regiment Club", addr:"10, KNC Rd, Gupta Colony, Barasat, West Bengal"},
      {name:"Nabapally Association Club", addr:"Colony More, Sarojinipally, Chakravartipara, Barasat"},
      {name:"Nabapally Amra Sobai Club", addr:"Nabapally, Barasat, West Bengal"},
      {name:"Amra Kajon Club", addr:"Rail Gate, Palpara, Barasat, West Bengal"},
      {name:"Sandhani Club", addr:"Prasadpur, Gupta Colony, Barasat, West Bengal"},
      {name:"Hariharpur United Club", addr:"Palpara, Barasat, West Bengal"},
      {name:"Jagriti Sangha", addr:"Krishnanagar Rd, Palpara, Barasat, West Bengal"},
      {name:"Taruchhaya Club", addr:"Ashok Colony, Bhatrapally, Barasat, West Bengal"},
      {name:"South Vatra Palli Cultural Association", addr:"Bhatrapally, Barasat, West Bengal"}
    ];

    const listEl = document.getElementById('list');
    const searchEl = document.getElementById('search');
    const clearBtn = document.getElementById('clearBtn');

    function createCard(club){
      const div = document.createElement('div');
      div.className = 'card';
      div.innerHTML = `
        <div style="display:flex;justify-content:space-between;align-items:center">
          <div>
            <h3>${escapeHtml(club.name)}</h3>
            <div class="addr">${escapeHtml(club.addr)}</div>
          </div>
          <div style="display:flex;flex-direction:column;gap:8px;align-items:flex-end">
            <button class="openmap" data-addr="${encodeURIComponent(club.addr)}">Open in Google Maps</button>
            <div class="icon" title="open maps">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="12" cy="9" r="2.2" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>
        </div>
      `;

      // click on card opens maps too
      div.querySelector('.openmap').addEventListener('click', (e)=>{
        e.stopPropagation();
        const encoded = e.currentTarget.getAttribute('data-addr');
        openMapsFromAddress(decodeURIComponent(encoded));
      });

      div.addEventListener('click', ()=>{
        openMapsFromAddress(club.addr);
      });

      return div;
    }

    function render(list){
      listEl.innerHTML = '';
      if(list.length===0){
        listEl.innerHTML = '<div style="grid-column:1/-1;padding:24px;border-radius:12px;background:transparent;color:var(--muted);text-align:center">কোনো ক্লাব পাওয়া যায়নি। অনুগ্রহ করে খোঁজ পরিবর্তন করুন।</div>';
        return;
      }
      list.forEach(c=> listEl.appendChild(createCard(c)));
    }

    function openMapsFromAddress(address){
      // use Google Maps search URL — more robust than fixed coords if user wants to update later
      const q = encodeURIComponent(address + ', Barasat, West Bengal');
      const url = `https://www.google.com/maps/search/?api=1&query=${q}`;
      window.open(url, '_blank');
    }

    function escapeHtml(text){
      return text.replace(/[&<>\"]/g, (s)=> ({'&':'&amp;','<':'&lt;','>':'&gt;','\\':'\\\\','"':'&quot;'})[s]);
    }

    // initial render
    render(clubs);

    // search
    searchEl.addEventListener('input', ()=>{
      const v = searchEl.value.trim().toLowerCase();
      const filtered = clubs.filter(c=> c.name.toLowerCase().includes(v) || c.addr.toLowerCase().includes(v));
      render(filtered);
    });

    clearBtn.addEventListener('click', ()=>{searchEl.value=''; render(clubs); searchEl.focus();});

  </script>
</body>
</html>
