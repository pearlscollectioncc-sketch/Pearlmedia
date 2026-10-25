# Pearls Collection – social media posts

Images in `posts/<week-folder>/` are fetched by Metricool from
`https://raw.githubusercontent.com/pearlscollectioncc-sketch/Pearlmedia/main/posts/<folder>/<file>.jpg`.

## Weekly routine (every Sunday)
1. Hospitable: get reviews from the past 7 days for all 5 homes (703, 506, 110, 412, 809). Pick the best 5-star review with real wording; quote it word for word (trim only, never reword), no guest names. Photo: that home's living room in `toolkit/photos/`.
2. Plan 3 posts for Mon/Wed/Fri 19:00 Asia/Dubai: guest review, owner tip (`type: tip`, 3 Q&As), home spotlight (`type: spotlight`, rotate 703 → 506 → 110 → 412 → 809, check last week's folder).
3. Write a spec JSON and run `python3 toolkit/make_week.py spec.json`, look at every image, then commit and push.
4. Create the posts in Metricool (brand 7622198, providers facebook + instagram, instagramData isAiGenerated false) with `draft: true`.
5. Send Olya the 3 images and captions to approve. Only after she says OK, switch them to scheduled (draft false). Never publish without her OK.

## Rules
- Only earnings claim allowed: "on average 30% more than renting long term". No revenue figures, no fees/commission, no utilities talk, no number of homes.
- Ratings: "4.9 on Airbnb", reviews "140+" (total Airbnb + Booking.com). Never "4.9 from 140+".
- Owner-facing posts: do not mention "Water's Edge". Building names are fine in home spotlights (guest-facing).
- Contact: WhatsApp +971 58 611 8979, pearlscollection.cc@gmail.com, website pearlscollection.netlify.app, DCT permit PER26000456.
- No AI-generated people or rooms; only real photos of the homes. No Airbnb logo (the words "Airbnb Superhost" are fine).
- Brand: cream #F4EDE2, espresso #2A1E14, gold #A9824A; Cormorant Garamond headings, Jost text, Cinzel wordmark.
- Hashtags: 4 max, e.g. #AbuDhabi #YasIsland #HolidayHomes #PropertyManagement.
