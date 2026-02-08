/**
 * Cookie Consent Manager
 */
class CookieConsent {
  constructor() {
    this.banner = document.getElementById("cookie-consent-banner");
    this.acceptBtn = document.getElementById("cookie-accept");
    this.rejectBtn = document.getElementById("cookie-reject");
    this.cookieName = "crawlio_cookie_consent";

    if (this.banner && !this.getCookie(this.cookieName)) {
      this.init();
    }
  }

  init() {
    // Delay appearance slightly for better UX
    setTimeout(() => {
      this.banner.style.display = "block";
    }, 1000);

    if (this.acceptBtn) {
      this.acceptBtn.addEventListener("click", () => this.acceptAll());
    }
    if (this.rejectBtn) {
      this.rejectBtn.addEventListener("click", () => this.rejectAll());
    }
  }

  acceptAll() {
    this.setConsent("accepted");
  }

  rejectAll() {
    this.setConsent("rejected");
  }

  setConsent(status) {
    this.setCookie(this.cookieName, status, 365);
    this.banner.style.opacity = "0";
    setTimeout(() => {
      this.banner.style.display = "none";
    }, 500);
  }

  setCookie(name, value, days) {
    let expires = "";
    if (days) {
      const date = new Date();
      date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
      expires = "; expires=" + date.toUTCString();
    }
    document.cookie =
      name + "=" + (value || "") + expires + "; path=/; SameSite=Lax";
  }

  getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(";");
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == " ") c = c.substring(1, c.length);
      if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
  }
}

// Initialize on DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
  new CookieConsent();
});
