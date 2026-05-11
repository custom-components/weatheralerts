class WeatherAlertsAlertCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._config = {};
    this._hass = null;
    this._index = 0;
    this._timer = null;
    this._tickerFrame = null;
    this._lastSignature = "";
    this._hasRendered = false;
    this._rotationSerial = 0;
    this._rotationAnimation = null;
    this._tickerAnimation = null;
    this._tickerAnchorIndex = 0;
    this._tickerTimelineKey = "";
    this._tickerTimelineStart = null;
    this._tickerReconnectScheduled = false;
    this._suppressNextEnterAnimation = false;
  }

  static getStubConfig(hass) {
    const entity = Object.keys(hass?.states || {}).find((id) => {
      const state = hass.states[id];
      return id.startsWith("sensor.weatheralerts") || state?.attributes?.integration === "weatheralerts";
    });

    return {
      type: "custom:weatheralerts-alert-card",
      entity: entity || "sensor.weatheralerts",
      display_mode: "rotating",
      content_mode: "compact",
      show_icon: true,
      show_alert_count: true,
      show_when_empty: false,
    };
  }

  setConfig(config) {
    if (!config || !config.entity) {
      throw new Error("WeatherAlerts Alert Card requires an entity");
    }

    this._config = {
      display_mode: "rotating",
      content_mode: "compact",
      headline_source: "title",
      rotation_interval: 7,
      rotation_pause: 0,
      rotation_type: "fold",
      rotation_animation_duration: "450ms",
      ticker_pixels_per_second: 70,
      ticker_start_position: "visible",
      ticker_loop_gap: "full",
      ticker_pause_on_hover: true,
      show_title: false,
      title: "Weather Alerts",
      show_icon: true,
      show_alert_count: true,
      show_navigation: true,
      show_when_empty: false,
      empty_message: "No active weather alerts",
      max_alerts: 10,
      warning_color: "#ff2020",
      watch_color: "#ff8800",
      advisory_color: "#ff8800",
      other_color: "#efbf00",
      no_alert_color: "#55cc00",
      warning_text_color: "#ffffff",
      watch_text_color: "#ffffff",
      advisory_text_color: "#ffffff",
      other_text_color: "#ffffff",
      no_alert_text_color: "#ffffff",
      warning_muted_text_color: "rgba(255,255,255,0.82)",
      watch_muted_text_color: "rgba(255,255,255,0.82)",
      advisory_muted_text_color: "rgba(255,255,255,0.82)",
      other_muted_text_color: "rgba(255,255,255,0.82)",
      no_alert_muted_text_color: "rgba(255,255,255,0.82)",
      border_radius: "12px",
      section_gap: "6px",
      ...config,
    };

    this._index = 0;
    this._hasRendered = false;
    this._resetTimer();
    this._render();
  }

  set hass(hass) {
    this._hass = hass;
    const alerts = this._getAlerts();
    const signature = JSON.stringify(alerts.map((a) => [a.id, a.title, a.NWSheadline, a.event, a.expires]));

    if (signature !== this._lastSignature || !this._hasRendered) {
      this._lastSignature = signature;
      if (this._index >= alerts.length) this._index = 0;
      this._resetTimer();
      this._render();
    }
  }

  connectedCallback() {
    if (this._tickerReconnectScheduled) return;
    this._tickerReconnectScheduled = true;
    window.requestAnimationFrame(() => {
      this._tickerReconnectScheduled = false;
      if (!this.isConnected || this._mode() !== "ticker") return;
      this._setupTickerAnimation();
    });
  }

  disconnectedCallback() {
    this._clearTimer();
    this._clearTickerFrame();
  }

  getCardSize() {
    const mode = this._mode();
    const contentMode = this._contentMode();
    if (contentMode === "full") return 5;
    if (mode === "list" || mode === "full") return 3;
    return 1;
  }

  _mode() {
    const mode = String(this._config.display_mode || "rotating").toLowerCase();
    return ["rotating", "ticker", "list", "full"].includes(mode) ? mode : "rotating";
  }

  _contentMode() {
    const mode = String(this._config.content_mode || "compact").toLowerCase();
    if (this._mode() === "full") return "full";
    return ["compact", "summary", "full"].includes(mode) ? mode : "compact";
  }

  _rotationType() {
    const configured = this._config.rotation_type ?? "fold";
    const value = String(configured).toLowerCase().replace(/-/g, "_");
    const type = value;
    const allowed = [
      "none",
      "fade",
      "slide_left",
      "slide_right",
      "slide_up",
      "slide_down",
      "fold",
      "flip",
      "zoom",
      "bounce",
      "blur",
      "roll",
      "twirl_left",
      "twirl_right",
    ];
    return allowed.includes(type) ? type : "fold";
  }

  _getAlerts() {
    if (!this._hass || !this._config?.entity) return [];
    const stateObj = this._hass.states[this._config.entity];
    const alerts = Array.isArray(stateObj?.attributes?.alerts) ? stateObj.attributes.alerts : [];
    const max = Number(this._config.max_alerts || 0);
    return max > 0 ? alerts.slice(0, max) : alerts;
  }

  _clearTimer() {
    if (this._timer) {
      window.clearTimeout(this._timer);
      this._timer = null;
    }
  }

  _clearTickerFrame() {
    if (this._tickerFrame) {
      window.cancelAnimationFrame(this._tickerFrame);
      this._tickerFrame = null;
    }
    if (this._tickerAnimation) {
      this._tickerAnimation.cancel();
      this._tickerAnimation = null;
    }
  }

  _resetTimer() {
    this._clearTimer();
    if (this._mode() !== "rotating") return;
    this._scheduleNextRotation();
  }

  _scheduleNextRotation() {
    this._clearTimer();
    if (this._mode() !== "rotating") return;

    const alerts = this._getAlerts();
    if (alerts.length <= 1) return;

    const interval = Math.max(2, Number(this._config.rotation_interval || 7));
    const pause = Math.max(0, Number(this._config.rotation_pause || 0));
    const delay = (interval + pause) * 1000;

    this._timer = window.setTimeout(() => {
      this._rotateBy(1, false, () => this._scheduleNextRotation());
    }, delay);
  }

  _nextAlert() {
    this._rotateBy(1, true);
  }

  _previousAlert() {
    this._rotateBy(-1, true);
  }

  _rotateBy(delta, resetAfter = false, done = null) {
    const alerts = this._getAlerts();
    if (alerts.length <= 1) {
      if (done) done();
      return;
    }

    const nextIndex = (this._index + delta + alerts.length) % alerts.length;
    const section = this.shadowRoot?.querySelector(".rotating-wrap .alert-section");
    const wrap = this.shadowRoot?.querySelector(".rotating-wrap");
    const type = this._rotationType();
    const duration = this._durationToMs(this._config.rotation_animation_duration || "450ms", 450);

    const finish = () => {
      this._index = nextIndex;
      this._rotationSerial += 1;
      this._render();
      if (resetAfter) this._resetTimer();
      if (done) done();
    };

    if (!section || type === "none" || duration <= 0) {
      finish();
      return;
    }

    if (this._rotationAnimation) {
      this._rotationAnimation.cancel();
      this._rotationAnimation = null;
    }

    if (type === "twirl_left" || type === "twirl_right") {
      this._runTwirlRotation(wrap, section, alerts[nextIndex], type, duration, finish);
      return;
    }

    const exitDuration = Math.max(120, Math.round(duration * 0.42));
    this._rotationAnimation = section.animate(this._rotationExitKeyframes(type, delta), {
      duration: exitDuration,
      easing: type === "bounce" ? "ease-in" : "ease",
      fill: "both",
    });

    this._rotationAnimation.onfinish = finish;
    this._rotationAnimation.oncancel = null;
  }

  _runTwirlRotation(wrap, currentSection, nextAlert, type, duration, finish) {
    if (!wrap || !currentSection || !nextAlert) {
      finish();
      return;
    }

    const sign = type === "twirl_right" ? -1 : 1;
    const template = document.createElement("template");
    template.innerHTML = this._alertSection(nextAlert, this._contentMode(), true);
    const incoming = template.content.firstElementChild;
    if (!incoming) {
      finish();
      return;
    }

    incoming.classList.add("twirl-incoming");
    incoming.style.setProperty("--alert-color", this._colorForAlert(nextAlert));
    incoming.style.setProperty("--alert-text-color", this._textColorForAlert(nextAlert));
    wrap.appendChild(incoming);
    wrap.classList.add("twirl-active");

    const easing = "cubic-bezier(.42,0,.18,1)";
    const outgoingFrames = [
      { opacity: 1, transform: "translateX(0) rotateY(0deg)", transformOrigin: sign >= 0 ? "left center" : "right center" },
      { opacity: 0.35, transform: `translateX(${-44 * sign}%) rotateY(${90 * sign}deg)`, transformOrigin: sign >= 0 ? "left center" : "right center" },
    ];
    const incomingFrames = [
      { opacity: 0.35, transform: `translateX(${44 * sign}%) rotateY(${-90 * sign}deg)`, transformOrigin: sign >= 0 ? "right center" : "left center" },
      { opacity: 1, transform: "translateX(0) rotateY(0deg)", transformOrigin: sign >= 0 ? "right center" : "left center" },
    ];

    const outgoingAnimation = currentSection.animate(outgoingFrames, {
      duration,
      easing,
      fill: "both",
    });
    const incomingAnimation = incoming.animate(incomingFrames, {
      duration,
      easing,
      fill: "both",
    });

    this._rotationAnimation = incomingAnimation;

    const cleanup = () => {
      outgoingAnimation.cancel();
      incomingAnimation.cancel();
      incoming.remove();
      wrap.classList.remove("twirl-active");
      this._rotationAnimation = null;
    };

    incomingAnimation.onfinish = () => {
      cleanup();
      this._suppressNextEnterAnimation = true;
      finish();
    };
    incomingAnimation.oncancel = null;
  }

  _render() {
    if (!this.shadowRoot || !this._config) return;

    const alerts = this._getAlerts();
    const stateObj = this._hass?.states?.[this._config.entity];
    const mode = this._mode();
    const contentMode = this._contentMode();

    if (!stateObj) {
      this.shadowRoot.innerHTML = this._styles() + this._error(`Entity not found: ${this._escape(this._config.entity)}`);
      this._hasRendered = true;
      return;
    }

    if (!alerts.length) {
      if (!this._config.show_when_empty) {
        this.shadowRoot.innerHTML = "";
        this._hasRendered = true;
        return;
      }
      this.shadowRoot.innerHTML = this._styles() + this._emptyCard();
      this._hasRendered = true;
      return;
    }

    let body = "";
    if (mode === "ticker") {
      body = this._ticker(alerts, contentMode);
    } else if (mode === "list" || mode === "full") {
      body = this._list(alerts, contentMode);
    } else {
      body = this._rotating(alerts, contentMode);
    }

    this.shadowRoot.innerHTML = this._styles() + `<ha-card>${this._header(alerts)}${body}</ha-card>`;
    this._wireNavigation();
    if (mode === "ticker") {
      this._setupTickerAnimation();
    } else {
      this._clearTickerFrame();
    }
    if (mode === "rotating") {
      this._setupRotationAnimation();
    }
    this._hasRendered = true;
  }

  _wireNavigation() {
    this.shadowRoot.querySelector(".previous")?.addEventListener("click", () => this._previousAlert());
    this.shadowRoot.querySelector(".next")?.addEventListener("click", () => this._nextAlert());
  }

  _header(alerts) {
    if (!this._config.show_title && !this._config.show_alert_count) return "";
    const count = alerts.length;
    const title = this._config.show_title ? `<div class="card-title">${this._escape(this._config.title || "Weather Alerts")}</div>` : "";
    const badge = this._config.show_alert_count ? `<div class="count">${count}</div>` : "";
    return `<div class="header">${title}<div class="spacer"></div>${badge}</div>`;
  }

  _emptyCard() {
    const bg = this._escape(this._config.no_alert_color || "#55cc00");
    const color = this._escape(this._config.no_alert_text_color || "#ffffff");
    return `<ha-card><div class="empty" style="--alert-color:${bg}; --alert-text-color:${color}; --alert-muted-text-color:${this._escape(this._config.no_alert_muted_text_color || "rgba(255,255,255,0.82)")};"><ha-icon icon="mdi:weather-sunny"></ha-icon><span>${this._escape(this._config.empty_message)}</span></div></ha-card>`;
  }

  _error(message) {
    return `<ha-card><div class="error">${message}</div></ha-card>`;
  }

  _rotating(alerts, contentMode) {
    const alert = alerts[this._index] || alerts[0];
    const transition = `rotation-${this._rotationType().replace(/_/g, "-")}`;
    const nav = this._config.show_navigation && alerts.length > 1
      ? `<button class="nav previous" aria-label="Previous alert">‹</button><button class="nav next" aria-label="Next alert">›</button>`
      : "";
    const counter = alerts.length > 1 ? `<div class="counter">${this._index + 1}/${alerts.length}</div>` : "";
    return `<div class="rotating-wrap ${transition}" data-rotation-run="${this._rotationSerial}">${this._alertSection(alert, contentMode, true)}${counter}${nav}</div>`;
  }

  _ticker(alerts, contentMode) {
    const parts = alerts.map((alert) => this._alertSection(alert, contentMode, false, "ticker-item")).join("");

    return `
      <div class="ticker-window">
        <div class="ticker-track">
          <div class="ticker-content ticker-content-primary">${parts}</div>
        </div>
      </div>
    `;
  }

  _setupTickerAnimation() {
    this._clearTickerFrame();
    this._tickerFrame = window.requestAnimationFrame(() => {
      this._tickerFrame = null;
      const windowEl = this.shadowRoot?.querySelector(".ticker-window");
      const trackEl = this.shadowRoot?.querySelector(".ticker-track");
      const contentEl = this.shadowRoot?.querySelector(".ticker-content-primary")
        || this.shadowRoot?.querySelector(".ticker-content");
      if (!windowEl || !trackEl || !contentEl) return;

      const viewportWidth = Math.max(1, windowEl.clientWidth);
      if (viewportWidth <= 1) {
        this._tickerFrame = window.requestAnimationFrame(() => this._setupTickerAnimation());
        return;
      }

      const contentWidth = Math.max(
        1,
        contentEl.scrollWidth,
        contentEl.getBoundingClientRect?.().width || 0
      );
      const pixelsPerSecond = this._tickerPixelsPerSecond();
      const gap = this._tickerLoopGapPixels(viewportWidth);
      const startsOffscreen = String(this._config.ticker_start_position || "visible").toLowerCase() === "offscreen";
      const period = Math.max(1, contentWidth + gap);

      trackEl.style.setProperty("--ticker-gap", `${gap}px`);
      const anchorIndex = this._syncTickerCopies(trackEl, contentEl, viewportWidth, contentWidth, gap);
      this._tickerAnchorIndex = anchorIndex;
      trackEl.style.visibility = "visible";

      // Offscreen mode starts the anchor copy just outside the right edge.
      // The strip also includes leading copies before the anchor so restoring or
      // wrapping phase never removes a partly visible copy on the left side.
      const start = startsOffscreen ? viewportWidth : 0;
      const timelineKey = this._tickerTimelineStorageKey(contentEl.innerText || contentEl.textContent || "");
      const timelineStart = this._ensureTickerTimelineStart(timelineKey);
      this._runTickerAnimation(trackEl, windowEl, start, period, pixelsPerSecond, anchorIndex, timelineKey, timelineStart);
    });
  }

  _syncTickerCopies(trackEl, contentEl, viewportWidth, contentWidth, gap) {
    const period = Math.max(1, contentWidth + gap);

    // Keep enough copies before and after the active anchor copy. This is the
    // important part for offscreen mode: when the phase wraps or a dashboard view
    // is rebuilt, a copy that was partly visible on the left still has an
    // equivalent leading copy in the same visual position.
    const beforeCopies = Math.max(8, Math.ceil((viewportWidth + contentWidth) / period) + 4);
    const afterCopies = Math.max(8, Math.ceil((viewportWidth + contentWidth) / period) + 4);
    const requiredCopies = beforeCopies + 1 + afterCopies;

    const existingCopies = Array.from(trackEl.querySelectorAll(".ticker-content-copy"));
    while (existingCopies.length > Math.max(0, requiredCopies - 1)) {
      existingCopies.pop()?.remove();
    }

    while (trackEl.querySelectorAll(".ticker-content").length < requiredCopies) {
      const clone = contentEl.cloneNode(true);
      clone.classList.remove("ticker-content-primary");
      clone.classList.add("ticker-content-copy");
      clone.setAttribute("aria-hidden", "true");
      trackEl.appendChild(clone);
    }

    return beforeCopies;
  }

  _runTickerAnimation(trackEl, windowEl, start, period, pixelsPerSecond, anchorIndex, timelineKey, timelineStart) {
    if (!trackEl || !windowEl || !this.isConnected) return;

    if (this._tickerAnimation?.cancel) {
      this._tickerAnimation.cancel();
    }
    this._tickerAnimation = null;

    let paused = false;
    let cancelled = false;
    let pausedPhase = null;

    const phaseFromClock = () => {
      const elapsed = Math.max(0, Date.now() - timelineStart);
      return ((elapsed * pixelsPerSecond) / 1000) % period;
    };

    const setPosition = (phase) => {
      const x = start - phase - (anchorIndex * period);
      trackEl.style.transform = `translate3d(${x}px, 0, 0)`;
    };

    const step = () => {
      if (cancelled || !this.isConnected || this._mode() !== "ticker") return;

      const phase = paused ? (pausedPhase ?? phaseFromClock()) : phaseFromClock();
      setPosition(phase);
      this._tickerFrame = window.requestAnimationFrame(step);
    };

    const controller = {
      pause: () => {
        if (!paused) {
          pausedPhase = phaseFromClock();
          paused = true;
        }
      },
      play: () => {
        if (paused) {
          // Shift the wall-clock timeline so the saved phase becomes the current
          // phase. This resumes hover pauses without jumping or counting paused time.
          const phase = pausedPhase ?? 0;
          const now = Date.now();
          const newStart = now - ((phase / pixelsPerSecond) * 1000);
          this._writeTickerTimelineStart(timelineKey, newStart);
          timelineStart = newStart;
          paused = false;
          pausedPhase = null;
        }
      },
      cancel: () => {
        cancelled = true;
      },
    };
    this._tickerAnimation = controller;

    const pause = () => this._tickerAnimation?.pause?.();
    const play = () => this._tickerAnimation?.play?.();
    if (this._config.ticker_pause_on_hover !== false && !windowEl.dataset.waHoverBound) {
      windowEl.addEventListener("mouseenter", pause);
      windowEl.addEventListener("mouseleave", play);
      windowEl.dataset.waHoverBound = "true";
    }

    setPosition(phaseFromClock());
    this._tickerFrame = window.requestAnimationFrame(step);
  }

  _tickerTimelineStorageKey(contentText) {
    const data = [
      this._config.entity || "",
      this._config.display_mode || "ticker",
      this._config.content_mode || "compact",
      this._config.ticker_start_position || "visible",
      this._config.ticker_loop_gap ?? this._config.ticker_gap ?? "full",
      this._config.headline_source || "title",
      contentText || "",
    ].join("|");

    let hash = 0;
    for (let i = 0; i < data.length; i += 1) {
      hash = ((hash << 5) - hash + data.charCodeAt(i)) | 0;
    }
    return `weatheralerts:tickerTimeline:${Math.abs(hash)}`;
  }

  _ensureTickerTimelineStart(key) {
    try {
      const stored = Number(window.sessionStorage?.getItem(key));
      if (Number.isFinite(stored) && stored > 0) return stored;
    } catch (_err) {
      // Ignore storage access errors. The ticker can still run with memory state.
    }

    const start = Date.now();
    this._writeTickerTimelineStart(key, start);
    return start;
  }

  _writeTickerTimelineStart(key, value) {
    try {
      window.sessionStorage?.setItem(key, String(value));
    } catch (_err) {
      // Ignore storage access errors.
    }
  }

  _tickerLoopGapPixels(viewportWidth) {
    const configured = this._config.ticker_loop_gap ?? this._config.ticker_gap ?? "full";
    if (typeof configured === "number") return Math.max(0, configured);

    const value = String(configured || "full").trim().toLowerCase();
    if (value.endsWith("px")) return Math.max(0, Number.parseFloat(value) || 0);
    if (value.endsWith("%")) return Math.max(0, viewportWidth * ((Number.parseFloat(value) || 0) / 100));
    if (["none", "no", "zero", "0"].includes(value)) return 0;
    if (["small", "little", "tight"].includes(value)) return 24;
    if (["half", "50", "50%"].includes(value)) return Math.round(viewportWidth / 2);
    if (["full", "offscreen", "100", "100%"].includes(value)) return viewportWidth;

    const numeric = Number.parseFloat(value);
    return Number.isFinite(numeric) ? Math.max(0, numeric) : viewportWidth;
  }


  _setupRotationAnimation() {
    if (this._suppressNextEnterAnimation) {
      this._suppressNextEnterAnimation = false;
      return;
    }
    const section = this.shadowRoot?.querySelector(".rotating-wrap .alert-section");
    if (!section || this._rotationType() === "none") return;

    if (this._rotationAnimation) {
      this._rotationAnimation.cancel();
      this._rotationAnimation = null;
    }

    const duration = this._durationToMs(this._config.rotation_animation_duration || "450ms", 450);
    const frames = this._rotationKeyframes(this._rotationType());
    this._rotationAnimation = section.animate(frames, {
      duration,
      easing: this._rotationType() === "bounce" ? "cubic-bezier(.22,1.2,.36,1)" : "ease",
      fill: "both",
    });
  }

  _durationToMs(value, fallback) {
    if (typeof value === "number") return Math.max(0, value);
    const text = String(value || "").trim().toLowerCase();
    if (!text) return fallback;
    if (text.endsWith("ms")) return Math.max(0, Number.parseFloat(text) || fallback);
    if (text.endsWith("s")) return Math.max(0, (Number.parseFloat(text) || fallback / 1000) * 1000);
    return Math.max(0, Number.parseFloat(text) || fallback);
  }

  _rotationKeyframes(type) {
    const commonEnd = { opacity: 1, transform: "none", filter: "none" };
    const map = {
      fade: [{ opacity: 0 }, { opacity: 1 }],
      slide_left: [{ opacity: 0.35, transform: "translateX(34px)" }, commonEnd],
      slide_right: [{ opacity: 0.35, transform: "translateX(-34px)" }, commonEnd],
      slide_up: [{ opacity: 0.35, transform: "translateY(22px)" }, commonEnd],
      slide_down: [{ opacity: 0.35, transform: "translateY(-22px)" }, commonEnd],
      fold: [{ opacity: 0.35, transform: "rotateX(-76deg)" }, commonEnd],
      flip: [{ opacity: 0.35, transform: "rotateY(-92deg)" }, commonEnd],
      zoom: [{ opacity: 0.25, transform: "scale(0.84)" }, commonEnd],
      bounce: [
        { opacity: 0, transform: "translateY(18px) scale(0.96)" },
        { opacity: 1, transform: "translateY(-5px) scale(1.015)", offset: 0.65 },
        commonEnd,
      ],
      blur: [{ opacity: 0.25, filter: "blur(8px)", transform: "scale(1.03)" }, commonEnd],
      roll: [{ opacity: 0.25, transform: "translateX(28px) rotate(5deg)" }, commonEnd],
      twirl_left: [{ opacity: 0.35, transform: "rotateY(76deg) translateX(22px)" }, commonEnd],
      twirl_right: [{ opacity: 0.35, transform: "rotateY(-76deg) translateX(-22px)" }, commonEnd],
    };
    return map[type] || map.fold;
  }

  _rotationExitKeyframes(type, direction = 1) {
    const sign = type === "twirl_right" ? -1 : 1;
    const map = {
      fade: [{ opacity: 1 }, { opacity: 0 }],
      slide_left: [{ opacity: 1, transform: "none" }, { opacity: 0, transform: `translateX(${-34 * sign}px)` }],
      slide_right: [{ opacity: 1, transform: "none" }, { opacity: 0, transform: `translateX(${34 * sign}px)` }],
      slide_up: [{ opacity: 1, transform: "none" }, { opacity: 0, transform: "translateY(-22px)" }],
      slide_down: [{ opacity: 1, transform: "none" }, { opacity: 0, transform: "translateY(22px)" }],
      fold: [{ opacity: 1, transform: "rotateX(0deg)" }, { opacity: 0.25, transform: "rotateX(76deg)" }],
      flip: [{ opacity: 1, transform: "rotateY(0deg)" }, { opacity: 0.25, transform: `rotateY(${92 * sign}deg)` }],
      zoom: [{ opacity: 1, transform: "scale(1)" }, { opacity: 0.2, transform: "scale(0.84)" }],
      bounce: [{ opacity: 1, transform: "translateY(0) scale(1)" }, { opacity: 0, transform: "translateY(-18px) scale(0.96)" }],
      blur: [{ opacity: 1, filter: "blur(0)", transform: "scale(1)" }, { opacity: 0.25, filter: "blur(8px)", transform: "scale(1.03)" }],
      roll: [{ opacity: 1, transform: "translateX(0) rotate(0deg)" }, { opacity: 0.25, transform: `translateX(${-28 * sign}px) rotate(${-5 * sign}deg)` }],
      twirl_left: [{ opacity: 1, transform: "rotateY(0deg) translateX(0)" }, { opacity: 0.25, transform: `rotateY(${-76 * sign}deg) translateX(${-22 * sign}px)` }],
      twirl_right: [{ opacity: 1, transform: "rotateY(0deg) translateX(0)" }, { opacity: 0.25, transform: `rotateY(${76 * sign}deg) translateX(${22 * sign}px)` }],
    };
    return map[type] || map.fold;
  }

  _tickerPixelsPerSecond() {
    const configured = this._config.ticker_pixels_per_second;
    return Math.max(10, Number(configured) || 70);
  }

  _list(alerts, contentMode) {
    return `<div class="list">${alerts.map((alert) => this._alertSection(alert, contentMode, false)).join("")}</div>`;
  }

  _alertSection(alert, contentMode, fill = false, extraClass = "") {
    const color = this._colorForAlert(alert);
    const textColor = this._textColorForAlert(alert);
    const mutedTextColor = this._mutedTextColorForAlert(alert);
    const text = this._primaryText(alert);
    const icon = this._config.show_icon ? `<ha-icon class="alert-icon" icon="${this._escape(alert.icon || "mdi:alert")}"></ha-icon>` : "";
    const classes = ["alert-section", fill ? "fill" : "", extraClass].filter(Boolean).join(" ");

    const summaryBlock = contentMode === "summary" ? this._summaryDetails(alert) : "";
    const fullBlock = contentMode === "full" ? this._fullDetails(alert) : "";

    return `
      <div class="${classes}" style="--alert-color:${this._escape(color)}; --alert-text-color:${this._escape(textColor)}; --alert-muted-text-color:${this._escape(mutedTextColor)};">
        <div class="alert-main">
          ${icon}
          <div class="alert-text">
            <div class="primary">${this._escape(text)}</div>
            ${summaryBlock}
          </div>
        </div>
        ${fullBlock}
      </div>
    `;
  }

  _fullDetails(alert) {
    const rows = [
      ["Event", alert.event],
      ["Area", alert.area],
      ["Severity", alert.severity],
      ["Urgency", alert.urgency],
      ["Certainty", alert.certainty],
      ["Effective", this._formatDate(alert.effective)],
      ["Expires", this._formatDate(alert.expires)],
    ].filter(([, value]) => this._hasValue(value));

    const rowsHtml = rows.map(([label, value]) => `<div class="detail-row"><span>${this._escape(label)}</span><strong>${this._escape(value)}</strong></div>`).join("");
    const description = this._hasValue(alert.description) ? `<div class="detail-block"><span>Description</span><p>${this._escape(alert.description)}</p></div>` : "";
    const instruction = this._hasValue(alert.instruction) ? `<div class="detail-block"><span>Instruction</span><p>${this._escape(alert.instruction)}</p></div>` : "";

    return `<div class="details">${rowsHtml}${description}${instruction}</div>`;
  }

  _primaryText(alert) {
    const source = String(this._config.headline_source || "title");
    return this._firstValue(alert[source], alert.title, alert.NWSheadline, alert.event, "Weather Alert");
  }

  _summaryDetails(alert) {
    const expires = this._formatDate(alert.expires);
    const parts = [alert.event, alert.area, expires ? `Expires ${expires}` : ""]
      .filter((value) => this._hasValue(value));
    return parts.length ? `<div class="summary">${this._escape(parts.join(" • "))}</div>` : "";
  }

  _firstValue(...values) {
    for (const value of values) {
      if (this._hasValue(value)) return String(value);
    }
    return "";
  }

  _hasValue(value) {
    return value !== undefined && value !== null && String(value).trim() !== "" && String(value).toLowerCase() !== "null";
  }

  _alertCategory(alert) {
    const text = `${alert.event || ""} ${alert.title || ""} ${alert.NWSheadline || ""}`.toLowerCase();
    if (text.includes("warning")) return "warning";
    if (text.includes("watch")) return "watch";
    if (text.includes("advisory")) return "advisory";
    return "other";
  }

  _colorForAlert(alert) {
    const category = this._alertCategory(alert);
    if (category === "warning") return this._config.warning_color;
    if (category === "watch") return this._config.watch_color;
    if (category === "advisory") return this._config.advisory_color;
    return this._config.other_color;
  }

  _textColorForAlert(alert) {
    const category = this._alertCategory(alert);
    if (category === "warning") return this._config.warning_text_color;
    if (category === "watch") return this._config.watch_text_color;
    if (category === "advisory") return this._config.advisory_text_color;
    return this._config.other_text_color;
  }

  _mutedTextColorForAlert(alert) {
    const category = this._alertCategory(alert);
    if (category === "warning") return this._config.warning_muted_text_color;
    if (category === "watch") return this._config.watch_muted_text_color;
    if (category === "advisory") return this._config.advisory_muted_text_color;
    return this._config.other_muted_text_color;
  }

  _formatDate(value) {
    if (!this._hasValue(value)) return "";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return String(value);
    return date.toLocaleString();
  }

  _styles() {
    const cfg = this._config || {};
    return `
      <style>
        :host {
          display: block;
          --wa-text-color: #ffffff;
          --wa-radius: ${this._escape(cfg.border_radius || "12px")};
          --wa-gap: ${this._escape(cfg.section_gap || "6px")};
          --wa-rotation-duration: ${this._escape(cfg.rotation_animation_duration || "450ms")};
          --wa-ticker-start: 100%;
          --wa-ticker-end: -100%;
          --wa-ticker-duration: 30s;
        }
        ha-card { overflow: hidden; }
        .header {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 10px 12px 0 12px;
        }
        .card-title {
          font-weight: 600;
          font-size: 16px;
        }
        .spacer { flex: 1; }
        .count, .counter {
          min-width: 28px;
          min-height: 22px;
          border-radius: 999px;
          background: var(--secondary-background-color, rgba(0,0,0,0.08));
          color: var(--primary-text-color);
          display: inline-flex;
          align-items: center;
          justify-content: center;
          font-size: 12px;
          font-weight: 700;
          padding: 0 8px;
        }
        .rotating-wrap {
          position: relative;
          padding: 12px;
          perspective: 900px;
        }
        .rotating-wrap .counter {
          position: absolute;
          right: 48px;
          top: 18px;
          background: rgba(0,0,0,0.22);
          color: var(--wa-text-color);
        }
        .list {
          display: flex;
          flex-direction: column;
          gap: var(--wa-gap);
          padding: 12px;
        }
        .alert-section {
          background: var(--alert-color);
          color: var(--alert-text-color, var(--wa-text-color));
          border-radius: var(--wa-radius);
          padding: 10px 12px;
          box-sizing: border-box;
          box-shadow: inset 0 0 0 1px rgba(255,255,255,0.16);
        }
        .alert-section.fill {
          min-height: 54px;
        }
        .alert-main {
          display: flex;
          align-items: center;
          gap: 10px;
        }
        .alert-icon {
          flex: 0 0 auto;
          --mdc-icon-size: 26px;
        }
        .alert-text {
          min-width: 0;
          flex: 1;
        }
        .primary {
          font-size: 16px;
          line-height: 1.25;
          font-weight: 700;
        }
        .summary {
          color: var(--alert-muted-text-color, rgba(255,255,255,0.82));
          margin-top: 3px;
          font-size: 13px;
          line-height: 1.28;
        }
        .details {
          margin-top: 10px;
          border-top: 1px solid rgba(255,255,255,0.28);
          padding-top: 8px;
          font-size: 13px;
          line-height: 1.35;
        }
        .detail-row {
          display: grid;
          grid-template-columns: minmax(88px, 130px) 1fr;
          gap: 8px;
          margin: 3px 0;
        }
        .detail-row span, .detail-block span {
          color: var(--alert-muted-text-color, rgba(255,255,255,0.82));
          font-weight: 600;
        }
        .detail-row strong {
          font-weight: 600;
        }
        .detail-block {
          margin-top: 8px;
        }
        .detail-block p {
          margin: 3px 0 0 0;
          white-space: pre-line;
        }
        .ticker-window {
          overflow: hidden;
          padding: 12px;
          min-height: 54px;
        }
        .ticker-track {
          display: flex;
          width: max-content;
          gap: var(--ticker-gap, 100%);
          will-change: transform;
          visibility: hidden;
        }
        .ticker-content {
          display: flex;
          flex: 0 0 auto;
          gap: var(--wa-gap);
          width: max-content;
        }
        .ticker-item {
          flex: 0 0 auto;
          min-width: max-content;
          max-width: 70vw;
        }
        .ticker-item .summary,
        .ticker-item .details {
          display: none;
        }
        .nav {
          position: absolute;
          top: 50%;
          transform: translateY(-50%);
          border: none;
          width: 28px;
          height: 36px;
          border-radius: 999px;
          background: rgba(0,0,0,0.22);
          color: var(--wa-text-color);
          font-size: 24px;
          line-height: 24px;
          cursor: pointer;
        }
        .nav:hover { background: rgba(0,0,0,0.34); }
        .previous { left: 16px; }
        .next { right: 16px; }
        .rotating-wrap .alert-section {
          padding-left: ${cfg.show_navigation === false ? "12px" : "42px"};
          padding-right: ${cfg.show_navigation === false ? "12px" : "72px"};
        }
        .empty, .error {
          padding: 14px;
          display: flex;
          align-items: center;
          gap: 10px;
        }
        .empty {
          background: var(--alert-color, #55cc00);
          color: var(--alert-text-color, #ffffff);
          margin: 12px;
          border-radius: var(--wa-radius);
          box-shadow: inset 0 0 0 1px rgba(255,255,255,0.16);
        }
        .error {
          color: var(--error-color, #db4437);
        }
        .rotating-wrap .alert-section {
          transform-origin: center;
          backface-visibility: hidden;
          will-change: transform, opacity, filter;
        }
        .rotation-fold .alert-section { transform-origin: top center; }
        .rotation-twirl-left {
          perspective: 1100px;
          transform-style: preserve-3d;
        }
        .rotation-twirl-left .alert-section { transform-origin: left center; }
        .rotation-twirl-right {
          perspective: 1100px;
          transform-style: preserve-3d;
        }
        .rotation-twirl-right .alert-section { transform-origin: right center; }
        .twirl-active {
          min-height: 54px;
        }
        .twirl-active .alert-section {
          position: relative;
          inset: auto;
        }
        .twirl-active .twirl-incoming {
          position: absolute;
          left: 12px;
          right: 12px;
          top: 12px;
          z-index: 2;
        }
        @keyframes waTicker {
          from { transform: translateX(var(--wa-ticker-start)); }
          to { transform: translateX(var(--wa-ticker-end)); }
        }
        @keyframes waFade {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes waSlideLeft {
          from { opacity: 0.35; transform: translateX(26px); }
          to { opacity: 1; transform: translateX(0); }
        }
        @keyframes waSlideRight {
          from { opacity: 0.35; transform: translateX(-26px); }
          to { opacity: 1; transform: translateX(0); }
        }
        @keyframes waSlideUp {
          from { opacity: 0.35; transform: translateY(18px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes waSlideDown {
          from { opacity: 0.35; transform: translateY(-18px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes waFold {
          from { opacity: 0.35; transform: rotateX(-72deg); }
          to { opacity: 1; transform: rotateX(0deg); }
        }
        @keyframes waFlip {
          from { opacity: 0.35; transform: rotateY(-90deg); }
          to { opacity: 1; transform: rotateY(0deg); }
        }
        @keyframes waZoom {
          from { opacity: 0.25; transform: scale(0.86); }
          to { opacity: 1; transform: scale(1); }
        }
        @keyframes waBounce {
          0% { opacity: 0; transform: translateY(16px) scale(0.96); }
          65% { opacity: 1; transform: translateY(-4px) scale(1.01); }
          100% { opacity: 1; transform: translateY(0) scale(1); }
        }
        @keyframes waBlur {
          from { opacity: 0.25; filter: blur(8px); transform: scale(1.03); }
          to { opacity: 1; filter: blur(0); transform: scale(1); }
        }
        @keyframes waRoll {
          from { opacity: 0.25; transform: translateX(22px) rotate(4deg); }
          to { opacity: 1; transform: translateX(0) rotate(0deg); }
        }
        @keyframes waTwirlLeft {
          from { opacity: 0.35; transform: rotateY(72deg) translateX(18px); }
          to { opacity: 1; transform: rotateY(0deg) translateX(0); }
        }
        @media (prefers-reduced-motion: reduce) {
          .ticker-track,
          .rotating-wrap .alert-section {
            animation: none !important;
          }
        }
        @media (max-width: 520px) {
          .rotating-wrap .alert-section {
            padding-left: 36px;
            padding-right: 52px;
          }
          .rotating-wrap .counter { display: none; }
          .primary { font-size: 15px; }
          .detail-row { grid-template-columns: 1fr; gap: 1px; }
        }
      </style>
    `;
  }

  _escape(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
}

customElements.define("weatheralerts-alert-card", WeatherAlertsAlertCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: "weatheralerts-alert-card",
  name: "WeatherAlerts Alert Card",
  description: "Display active WeatherAlerts integration alerts as a rotating card, ticker, list, or full alert display.",
});
