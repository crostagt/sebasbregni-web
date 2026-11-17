/* ==========================================================================
   SEBAS BREGNI PHOTOGRAPHY — CONTENT
   This is the only file to edit when adding work. The site rebuilds itself.

   1. Put the original photographs and videos in one folder.
   2. Run:  python3 tools/prepare_media.py <that-folder> --site site
   3. In a slot, set  img:"<file name in lowercase, spaces as dashes>"
      e.g. _MG_2066.jpg  ->  img:"mg-2066";  a film: video:"<name>", film:true
   Gallery covers in black and white: python3 tools/make_bw.py <photo> --site site

   A work:    { img, video, film, title, alt }
   A project: { title, client, year, works }   client and year only when confirmed
   A room:    { id, no, title, line, discipline, text, dark, cover, coverColor, projects }

   Curated 11 Nov 2026: 71 photographs and 7 films, chosen from 140.
   Added 16 Nov 2026: 17 photographs (Models: Low key, Smoke, Black on grey,
   Hola Guatemala, Studio; Food: Wood-fired).
   No client is named until Sebastián confirms it.
   ========================================================================== */

window.SITE = {
  whatsapp: "",            // international format, digits only. Empty = hidden.
  email: "",
  instagram: "sebasbregni_photography",
  hero: { img: "", alt: "" },
  // opening screen: one print per discipline, each opens its room
  heroSet: [
    { img: "cover-models2-bw", room: "people", label: "Fashion", alt: "Model in a floral kimono with a fan" },
    { img: "cover-jewelry-bw", room: "jewelry", label: "Watches", alt: "Chronograph on a fabric strap" },
    { img: "cover-motion-bw", room: "motion", label: "Motion", alt: "Motorcycle on black" },
    { img: "cover-products-bw", room: "objects", label: "Product", alt: "Can resting on ice" }
  ]
};

(function () {
  const p = (img, alt) => ({ img, alt: alt || "" });
  const f = (video, title) => ({ video, title, film: true });

  window.ROOMS = [
    { id: "objects", no: "01", title: "Products", line: "Product and still life", discipline: "Product / Still life",
      text: "Product photography. Light, reflection, texture and colour.",
      coverColor: "cover-products", cover: p("cover-products-bw", "Can resting on ice"),
      projects: [
        { title: "Cold light", works: [ p("cover-products"), p("coke-red"), p("g0a3455"), p("g0a3428") ] },
        { title: "Colour study", works: [ p("mg-1864"), p("mg-1965"), p("mg-1991") ] },
        { title: "Still life", works: [ p("mg-6168"), p("mg-6318") ] }
      ] },
    { id: "jewelry", no: "02", title: "Jewelry & Watches", line: "Detail and macro", discipline: "Watches / Jewelry", dark: true,
      text: "Watches and jewelry, close.",
      coverColor: "cover-jewelry", cover: p("cover-jewelry-bw", "Chronograph on a fabric strap"),
      projects: [
        { title: "Bird of paradise", works: [ p("g0a0187", "Earrings, bracelet and ring on bird of paradise flowers"), p("g0a0177", "Ring and pendant on a bird of paradise stem") ] },
        { title: "Citizen", works: [ p("cover-jewelry"), p("citizen-1"), p("citizen-3"), f("film-citizen", "Citizen"), p("g0a0005") ] },
        { title: "Jewelry", works: [ p("g0a3474"), p("0g0a3431") ] }
      ] },
    { id: "food", no: "03", title: "Food", line: "Restaurants and hotels", discipline: "Food / Hospitality",
      text: "Food photography from the garden to the table.",
      coverColor: "cover-food", cover: p("cover-food-bw", "Chocolate sauce poured over a layered chocolate cake"),
      projects: [
        { title: "Lake Atitlán", works: [ p("mg-1456"), p("mg-1381"), p("mg-1584"), p("mg-0786"), p("mg-0993"), p("mg-1055"), p("mg-1788"), p("mg-1736") ] },
        { title: "After dark", works: [ p("mg-5954"), p("mg-6033") ] },
        { title: "Wood-fired", works: [ p("g0a7916", "Margherita with basil and grated cheese, from above"), p("g0a8002", "Pizza with cured meat, capers and microgreens, from above"), p("g0a8036", "Pizza with anchovies, pickled peppers and basil, from above"),
                                        p("g0a7955", "Pizza dough stretched between two hands over a floured counter"), p("g0a7942", "Floured hands clapping above a ball of dough"), p("g0a7854", "Hand folding pizza dough on a floured counter") ] }
      ] },
    { id: "motion", no: "04", title: "Motion", line: "Machines in the dark", discipline: "Automotive", dark: true,
      text: "Motorcycles lit as sculpture.",
      coverColor: "cover-motion", cover: p("cover-motion-bw", "Triumph Speed Twin 1200 in three-quarter view on black"),
      projects: [
        { title: "Triumph Speed Twin 1200", works: [ p("triumph-34"), p("triumph-front"), f("film-triumph", "Triumph Speed Twin 1200") ] },
        { title: "Stark Varg", works: [ p("stark-side"), p("stark-front"), p("mg-2366"), p("mg-2270"), p("mg-2348") ] }
      ] },
    { id: "people", no: "05", title: "Models", line: "Fashion, beauty, portrait", discipline: "Fashion / Beauty",
      text: "Fashion, beauty and portraiture in the studio.",
      coverColor: "cover-models2", cover: p("cover-models2-bw", "Model in a floral kimono with a fan, next to an old wooden door"),
      projects: [
        { title: "Kimono", works: [ p("g0a7515", "Model in a floral kimono holding a fan, by an old wooden door"), p("g0a7542", "Kimono, fan and lace slip on a red backdrop"), p("g0a7549", "Kimono and fan, one knee raised, on red") ] },
        { title: "Silver on pink", works: [ p("g0a7646", "Model in a metallic dress, arms raised, on pink"), p("g0a7662", "Metallic dress and wind in the hair, on pink"), p("g0a7655", "Close portrait in a metallic dress, on pink") ] },
        { title: "Beauty", works: [ p("g0a3507"), p("g0a3507a"), p("g0a3513b") ] },
        { title: "Handbags", works: [ p("g0a4649"), p("g0a4791"), p("g0a5085"), p("g0a4974") ] },
        { title: "Rose", works: [ p("mg-6710"), p("mg-6651") ] },
        { title: "Linen and straw", works: [ p("mg-6547"), p("mg-6375") ] },
        { title: "Monochrome", works: [ p("mg-8319"), p("mg-8506"), p("mg-8239") ] },
        { title: "Low key", works: [ p("mg-1123", "Black and white portrait of a man in glasses holding headphones at his neck"), p("mg-1150", "Profile portrait in headphones, low key"), p("mg-1151", "Three-quarter portrait in headphones and glasses, low key") ] },
        { title: "Smoke", works: [ p("mg-1949", "Man in a hat and waistcoat exhaling smoke, low key"), p("mg-1947", "Man in a hat looking down at a curl of smoke") ] },
        { title: "Black on grey", works: [ p("mg-9340", "Model in a black crop top and jeans, looking over her shoulder"), p("mg-9276", "Beauty portrait, hand on the shoulder, on grey"), p("mg-9315", "Model seated on a stool in black, on grey") ] },
        { title: "Hola, Guatemala", works: [ p("mg-8464", "Model framed by hands, wearing a Hola Guatemala cap and woven top"), p("mg-8574", "Model in a green Hola Guatemala bucket hat, selfie angle") ] },
        { title: "Studio", works: [ p("cover-models"), p("mg-4143"), p("g0a8231"), p("mg-1022"), p("g0a8517", "Full-length portrait in black, hand on the hip") ] }
      ] },
    { id: "animals", no: "06", title: "Pets", line: "Dogs and cats in the studio", discipline: "Pets",
      text: "Pet photography: patience, light and real expressions.",
      coverColor: "mg-9076", cover: p("cover-pets-bw", "Tabby kitten on white"),
      projects: [
        { title: "Dogs", works: [ p("g0a4179-2"), p("g0a4282"), p("g0a4443"), p("g0a4218"), p("g0a8317") ] },
        { title: "Kittens", works: [ p("mg-9230"), p("mg-9113"), p("mg-9084"), p("mg-9076") ] }
      ] },
    { id: "nature", no: "07", title: "Nature", line: "Wildlife up close", discipline: "Nature / Macro", dark: true,
      text: "Snakes, insects and spiders, close and in their own light.",
      coverColor: "cover-nature", cover: p("cover-nature-bw", "Green viper, eye in close-up"),
      projects: [
        { title: "Snakes", works: [ p("img-8774", "Viper coiled among leaves"), p("img-8813", "Green viper with its tongue out over a curled leaf"), p("img-8815", "Green viper stretched across ferns"), p("img-8817", "Green viper resting on a fern"), p("img-8820", "Eye of a green viper, macro"), p("img-8820-v", "Green viper, eye and scales in close-up"), p("mg-5129", "Vine snake stretched across a black background") ] },
        { title: "Insects", works: [ p("g0a2055", "Leaf katydid on a dry leaf, front view"), p("g0a2060", "Leaf katydid in profile on a dry leaf"), p("mg-01384", "Head of a stick insect on black"), p("insecto-palo", "Stick insect walking on bark") ] },
        { title: "Spiders", works: [ p("g0a4261", "Orb-weaver spider on its web"), p("g0a4289", "Dark orb-weaver spider hanging from its thread"), p("g0a4319", "Legs and face of an orb-weaver spider, macro") ] }
      ] },
    { id: "weddings", no: "08", title: "Weddings", line: "Days that happen once", discipline: "Weddings",
      text: "A wedding from the dress to the first dance.",
      coverColor: "0g0a3682", cover: p("cover-weddings-bw", "Wedding dress hanging from a tree"),
      projects: [
        { title: "Wedding day", works: [ p("0g0a3694"), p("0g0a3682"), p("0g0a3548"), p("0g0a5123"), p("0g0a5155"), p("0g0a5171"), p("g0a5341"), p("0g0a4989"), p("0g0a5443") ] }
      ] },
    { id: "moving-image", no: "09", title: "Films", line: "Commercials and reels", discipline: "Film", dark: true,
      text: "Reels and commercial films. Select a frame to play it.",
      coverColor: "film-cover", cover: p("film-cover-bw", "Film still: a smiling girl"),
      projects: [
        { works: [ f("film-environment", "Defend your environment"), f("film-portrait", "Kitchen"), f("film-handbags-1", "Handbags, Monday to Friday"),
                   f("film-triumph", "Triumph Speed Twin 1200"), f("film-editorial", "Editorial"), f("film-citizen", "Citizen") ] }
      ] }
  ];
})();
