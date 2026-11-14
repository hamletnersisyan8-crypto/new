# Նախագծային կայք — Flask + GitHub + Render

## Ինչ կա նախագծում

- `app.py` — Flask սերվեր և այցելուների ծանուցում էլեկտրոնային փոստով
- `templates/index.html` — քո HTML կայքը
- `requirements.txt` — Python փաթեթներ
- `render.yaml` — Render-ի տեղակայման կարգավորումներ

## Կարևոր

GitHub-ը կպահի կոդը, բայց GitHub Pages-ը չի աշխատեցնում Python/Flask։
Այս նախագիծը տեղադրիր Render-ում՝ միացնելով GitHub repository-ն։

Մի՛ տեղադրիր իրական Gmail գաղտնաբառը կամ App Password-ը GitHub-ում։
Այն պահիր միայն Render → Environment բաժնում։

Քանի որ նախկին հաղորդագրության մեջ App Password էր հայտնվել, նախ չեղարկիր այն
Google Account-ի App passwords բաժնում և ստեղծիր նոր App Password։

## Տեղային գործարկում

1. Տեղադրիր Python-ը։
2. Տերմինալում՝

   ```bash
   pip install -r requirements.txt
   ```

3. Ստեղծիր environment variables՝ `.env` ֆայլի փոխարեն համակարգի կարգավորումներում
   կամ տերմինալում։ `.env.example`-ը միայն օրինակ է և ինքնաբերաբար չի բեռնվում։

   Windows PowerShell-ի համար՝

   ```powershell
   $env:SMTP_USER="your-gmail@gmail.com"
   $env:SMTP_PASS="your-new-app-password"
   $env:MAIL_TO="your-email@gmail.com"
   $env:TRUST_RENDER_PROXY="false"
   python app.py
   ```

4. Բացիր `http://127.0.0.1:5000/`։

## GitHub

1. GitHub-ում ստեղծիր նոր repository։
2. Վերբեռնիր այս թղթապանակի ֆայլերը (ոչ թե zip-ը՝ որպես միակ ֆայլ)։
3. Համոզվիր, որ `.env` կամ իրական գաղտնաբառ չկա repository-ում։

## Render

1. Render-ում ընտրիր **New → Web Service**։
2. Միացրու քո GitHub repository-ն։
3. Build Command՝ `pip install -r requirements.txt`
4. Start Command՝ `gunicorn app:app`
5. Environment բաժնում ավելացրու՝
   - `SMTP_HOST` = `smtp.gmail.com`
   - `SMTP_PORT` = `465`
   - `SMTP_USER` = քո Gmail հասցեն
   - `SMTP_PASS` = նոր Google App Password-ը
   - `MAIL_TO` = այն հասցեն, որտեղ ուզում ես ստանալ ծանուցումները
   - `TRUST_RENDER_PROXY` = `true`
6. Deploy արա։ Render-ը կտա կայքի հանրային հղումը։

## Նշումներ

- Նույն IP հասցեից առավելագույնը մեկ նամակ է ուղարկվում մեկ ժամում։
- Ծանուցման մեջ ներառվում են IP հասցեն, UTC ժամը, էջի հասցեն և դիտարկիչի User-Agent-ը։
- IP հասցեն անձնական տվյալ է։ Կայքի այցելուներին տեղեկացրու դրա հավաքման մասին և պահիր տվյալները
  միայն անհրաժեշտության դեպքում։
- Այս տարբերակում cooldown-ի տվյալները պահվում են հիշողության մեջ․ սերվերի վերագործարկումից հետո
  մեկ ժամվա սահմանափակումը զրոյանում է։
- Render-ի անվճար պլանը կարող է քնել անգործության ժամանակ, ուստի առաջին բացումը կարող է ուշանալ։
