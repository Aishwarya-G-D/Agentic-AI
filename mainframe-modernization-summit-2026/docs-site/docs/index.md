---
title: Mainframe Modernization Summit Handbook 2026
hide:
  - navigation
  - toc
---

<section class="tsh-hero" markdown>

<div class="tsh-hero__prompt"><span id="tsh-typed"></span><span class="tsh-hero__cursor">&nbsp;</span></div>

<div class="tsh-hero__ctas">
  <a class="tsh-btn tsh-btn--primary" href="setup/index.html">$ Setup</a>
  <a class="tsh-btn" href="troubleshooting/index.html">! Troubleshooting</a>
</div>

</section>

<div class="tsh-grid" markdown>

<div class="tsh-card" markdown>
### $ setup
Get your laptop, ADK, and z/OSMF connectivity ready before the first session.
[Start here →](setup/index.md)
</div>

<div class="tsh-card" markdown>
### ! troubleshoot
The exact errors you'll hit, and how to unblock yourself in under a minute.
[Browse fixes →](troubleshooting/index.md)
</div>

</div>

<script>
  document.addEventListener("DOMContentLoaded", function () {
    if (typeof Typed === "undefined") return;
    new Typed("#tsh-typed", {
      strings: [
        "&gt; welcome to the mainframe modernization summit 2026. <br>&gt;"
      ],
      typeSpeed: 35,
      backSpeed: 0,
      smartBackspace: false,
      showCursor: false,
      onComplete: function () {
        document.querySelector(".tsh-hero__cursor").style.display = "none";
      }
    });
  });
</script>
