"use strict";
function scrollToTop() {
    $("html, body").stop().animate({ scrollTop: 0 }, 1e3, "swing");
}
window.onpageshow = function (e) {
    e.persisted && window.location.reload();
};
const preloader = document.querySelector(".preloader");
function goBack() {
    document.referrer.includes(init.home_url) ? history.back() : (window.location.href = init.home_url);
}
function changeTitle(e) {
    var t = $(".projects__item").eq(e).find(".title").html();
    $(".projects__slider__overlay__inner .title").html(t);
}
function setTransform(e, t) {
    (e.style.transform = t), (e.style.willChange = t), (e.style.WebkitTransform = t);
}
window.addEventListener("load", function () {
    performance.getEntriesByType("navigation");
    preloader &&
        (sessionStorage.isVisited
            ? ((document.querySelector("body").style.overflow = ""),
              (document.querySelector(".preloadContainer").style.opacity = 1),
              document.querySelector(".preloadContainer").classList.remove("preload"),
              (document.querySelector(".home__intro__blur").style.transform = "translateX(0)"),
              (document.querySelector(".home__intro__blur").style.transition = "transform 0.8s cubic-bezier(0.215, 0.61, 0.355, 1)"),
              (document.querySelector(".home__intro__overlay .title").style.animation = "fadeIn 0.5s 0.3s ease backwards"),
              (document.querySelector(".home__intro__overlay .subtitle").style.animation = "fadeIn 0.5s 0.6s ease backwards"),
              document.querySelector(".home__intro__blur").addEventListener("transitionend", function () {
                  document.querySelector(".home__intro__blur").style.transition = "none";
              }),
              document.querySelector(".home__intro__video video").play())
            : (window.innerWidth <= 1024 && (preloader.style.height = Math.min(document.documentElement.clientHeight, window.screen.height, window.innerHeight) + "px"),
              (document.querySelector("body").style.overflow = "hidden"),
              preloader.classList.add("loading"),
              document.querySelector(".preloadContainer").classList.add("preload"),
              (document.querySelector(".home__intro__blur").style.transition = "transform 0.8s 3s cubic-bezier(0.215, 0.61, 0.355, 1)"),
              (document.querySelector(".home__intro__overlay .title").style.animation = "fadeIn 0.8s 3.5s ease backwards"),
              (document.querySelector(".home__intro__overlay .subtitle").style.animation = "fadeIn 0.8s 3.8s ease backwards"),
              (sessionStorage.isVisited = "true"),
              (preloader.style.opacity = "1"),
              (preloader.style.visibility = "visible"),
              preloader.addEventListener("transitionend", function () {
                  document.querySelector(".preloadContainer").classList.remove("hasPreload");
              }),
              setTimeout(function () {
                  (document.querySelector("body").style.overflow = ""),
                      preloader.classList.remove("loading"),
                      (preloader.style.opacity = "0"),
                      (preloader.innerHTML = ""),
                      (preloader.style.display = "none"),
                      (document.querySelector(".home__intro__blur").style.transition = ""),
                      document.querySelector(".home__intro__video video").play();
              }, 4e3)));
}),
    changeTitle(0);
let current = 0,
    target = 0,
    ease = 0.1,
    rafId = void 0,
    rafActive = !1;
function updateScroll() {
    (target = window.scrollY || window.pageYOffset), startAnimation();
}
function startAnimation() {
    rafActive || ((rafActive = !0), (rafId = requestAnimationFrame(updateAnimation)));
}
function updateAnimation() {
    var e = target - current,
        t = Math.abs(e) < 0.1 ? 0 : e * ease;
    return (
        t ? ((current += t), (current = parseFloat(current.toFixed(2))), (rafId = requestAnimationFrame(updateAnimation))) : ((current = target), (rafActive = !1), cancelAnimationFrame(rafId)),
        updateAnimationHomeHero(),
        animateHomeProjects(),
        animeElementsOnViewport(),
        animateCtaHome(),
        animateAboutHome(),
        animateProjectsSlider(),
        !1
    );
}
function animateProjectsSlider() {
    var e = $("#projects-archive"),
        t = e.find(".projects__item"),
        o = t.length;
    if (e.hasClass("projects__slider")) {
        var r = current,
            i = r / $(window).height(),
            s = r / ($(window).height() * o - 1),
            n = r / ($(window).height() * (o - 1)),
            c = Math.ceil(i - 0.95),
            l = 100 * o * -s,
            a = 0.02 + n,
            d = 0.96 - n;
        if (
            ($(".projects__slider__overlay .scrollbar__fill").css({ transform: "scaleX(" + a + ")" }),
            $(".projects__slider__overlay .scrollbar__empty").css({ transform: "scaleX(" + d + ")" }),
            changeTitle(c),
            t.each(function (e, r) {
                var i = $(this).find("img"),
                    s = $(this).index(),
                    n = $(this).find(".projects__item__darkOverlay"),
                    a = l / 100,
                    d = -500 * (s + a),
                    u = Math.abs((s + a) / 3);
                if (($(r).removeClass("isSelected"), $(t).eq(c).addClass("isSelected"), !(c >= o - 1))) {
                    u = Math.max(1, Math.min(1.5, u + 1));
                    var m = 0.75 * (s + a);
                    m < 0 && (m = -m), i.css({ transform: "translateX( " + d + "px) scale(" + u + ")" }), n.css({ opacity: "" + m });
                }
            }),
            (document.querySelector(".currentProject").innerHTML = Math.round(c + 1)),
            (document.querySelector(".totalProject").innerHTML = document.querySelectorAll(".projects__item").length),
            c >= o - 1)
        )
            return;
        e.css("transform", "translateX(" + l + "%)");
    }
}
window.addEventListener("scroll", updateScroll);
let previousScroll = 0;
const clamp = (e, t, o) => Math.min(Math.max(e, t), o);
function animateHomeProjects() {
    var e,
        t,
        o,
        r = $("#projects");
    if ((r = $("#projects")).length > 0 && window.innerWidth >= 768) {
        var i = r.offset().top,
            s = 0,
            n = r.find(".title"),
            c = r.find(".subtitle"),
            l = r.find(".scrollbar__fill"),
            a = r.find(".scrollbar__empty"),
            d = r.outerHeight();
        const g = document.querySelector(".selected-projects__overlay");
        g.getBoundingClientRect().right;
        var u = current,
            m = r.find(".selected-projects__slider").children(),
            _ = (u - i) / (d - $(window).height()),
            h = 0.02 + (_ = Math.min(Math.max(_, 0), 1)),
            y = 0.96 - _;
        l.css({ transform: "scaleX(" + h + ")" }), a.css({ transform: "scaleX(" + y + ")" });
        var p = $(window).width() * (m.length - 1) * _;
        $(".selected-projects__slider").css({ transform: "translateX(-" + p + "px)" });
        const w = m[(s = (s = p / $(window).width()) > Math.ceil(s) - 0.25 ? Math.ceil(s) : Math.floor(s))],
            S = m.find("img")[s],
            q = m.find(".rightGradient")[s],
            b = w.getBoundingClientRect().right;
        let j = (100 * b) / w.offsetWidth,
            L = (100 * b) / w.offsetWidth;
        if (s == m.length - 1) {
            j = (200 * w.getBoundingClientRect().bottom) / w.offsetWidth;
        }
        (j = 100 - j), (L = (L / 100) * 0.5 + 0.85);
        let k = j / 100;
        (j /= 200), (j = Math.max(1, Math.min(1.4, j + 1))), (e = L), (t = 1), (o = 1.4), (L = Math.min(Math.max(e, t), o)), (q.style.opacity = "" + k), (S.style.transform = `scale(${j})`);
        var f = m.eq(s).data("title"),
            v = m.eq(s).data("subtitle");
        s != m.length - 1 && (m[s + 1].querySelector("img").style.transform = `scale(${L})`),
            previousScroll < u
                ? p / $(window).width() > Math.ceil(p / $(window).width()) - 0.25 && j >= 1
                    ? (n.text(f),
                      c.text(v),
                      (g.querySelector(".currentProject").innerText = s + 1),
                      (n[0].style.animation = "fadeIn 0.8s ease-out backwards"),
                      (c[0].style.animation = "fadeIn 0.8s 0.1s ease-out backwards"),
                      (g.querySelector(".currentProject").style.animation = "fadeIn 0.8s ease-out backwards"))
                    : p / $(window).width() > Math.ceil(p / $(window).width()) - 0.28 &&
                      j >= 1 &&
                      ((n[0].style.animation = "fadeOut 0.8s ease-in both "),
                      (c[0].style.animation = "fadeOut 0.8s 0.1s ease-in both "),
                      (g.querySelector(".currentProject").style.animation = "fadeOut 0.8s 0.1s ease-in both "),
                      n.text(f),
                      c.text(v),
                      (g.querySelector(".currentProject").innerText = s + 1))
                : p / $(window).width() < Math.ceil(p / $(window).width()) - 0.28 && j >= 1
                ? (n.text(f),
                  c.text(v),
                  (n[0].style.animation = "fadeIn 0.8s ease-out backwards"),
                  (c[0].style.animation = "fadeIn 0.8s ease-out backwards"),
                  (g.querySelector(".currentProject").innerText = s + 1),
                  (g.querySelector(".currentProject").style.animation = "fadeIn 0.8s ease-out backwards"))
                : p / $(window).width() < Math.ceil(p / $(window).width()) - 0.25 &&
                  j >= 1 &&
                  ((n[0].style.animation = "fadeOut 0.8s ease-in both"),
                  (c[0].style.animation = "fadeOut 0.8s 0.1s ease-in both"),
                  (g.querySelector(".currentProject").style.animation = "adeOut 0.8s 0.1s ease-in both"),
                  c[0].addEventListener("animationend", () => {
                      n.text(f), c.text(v), (g.querySelector(".currentProject").innerText = s + 1);
                  })),
            (previousScroll = u);
    }
}
function updateAnimationHomeHero() {
    const e = document.querySelector(".home__intro");
    if (e) {
        const t = e.querySelector(".home__intro__blur"),
            o = e.querySelector(".title"),
            r = e.querySelector(".subtitle"),
            i = e.querySelector(".btn__showreel"),
            s = e.querySelector(".scrollbar__container"),
            n = e.querySelector(".scrollbar__fill"),
            c = e.querySelector(".scrollbar__empty"),
            l = e.querySelector(".home__intro__overlay").clientHeight;
        let a,
            d,
            u = 1 - current / (l / 10);
        (u = Math.min(Math.max(u, 0), 1)),
            (a = Math.min(Math.max(-10 * (1 - u), -10), 0)),
            (d = Math.min(Math.max(0.2 * -current, -20), 0)),
            setTransform(t, "translateX(" + a + "%)"),
            (t.style.opacity = u),
            setTransform(o, "translateY(" + d + "%)"),
            (o.style.opacity = u),
            setTransform(r, "translateY(" + d + "%)"),
            (r.style.opacity = u),
            setTransform(i, "translateY(" + d + "%)"),
            (i.style.opacity = u);
        let m = current / (e.clientHeight - window.innerHeight),
            _ = Math.min(Math.max(m, 0), 1),
            h = 0.02 + _,
            y = 0.96 - _;
        const p = e.querySelector(".scrollbar__text");
        p.innerHTML = _ < 0.5 ? s.dataset.start : _ >= 1 ? s.dataset.finish : s.dataset.halfway;
        let f = (current - e.getClientRects()[0].bottom) / (e.clientHeight - window.innerHeight);
        (f = 1 - f), (f = Math.min(Math.max(f, 0), 1)), (e.querySelector(".topGradient").style.opacity = 0.4 * f), (s.style.opacity = f), setTransform(n, "scaleX(" + h + ")"), setTransform(c, "scaleX(" + y + ")");
    }
}
const animateAboutHome = () => {
        let e = document.querySelector(".home__about .content");
        if (e) {
            let t = e.querySelector(".textcolumn"),
                o = e.getClientRects()[0].bottom,
                r = 1 - (current - o) / (document.querySelector(".home__intro").getClientRects()[0].bottom - window.innerHeight);
            (r = Math.min(Math.max(r, 0), 1)),
                (e.style.opacity = r),
                [...t.children].forEach((e) => {
                    e.style.opacity = r;
                });
        }
    },
    animateCtaHome = () => {
        var e = document.querySelector(".cta__items");
        let t = 0;
        document.querySelectorAll("#cta").forEach((o) => {
            if (window.innerWidth >= 768) {
                var r = o,
                    i = 0;
                [...e.children].forEach((e) => {
                    i += e.offsetWidth;
                });
                var s = e.offsetLeft;
                (i += s), (r.style.height = i + "px");
                var n = r.offsetTop,
                    c = current,
                    l = (c - n) / (i - $(window).height());
                l = Math.min(Math.max(l, 0), 1);
                var a = (i - $(window).width()) * l * 1.2;
                setTransform(e, `translateX(-${a}px)`);
                var d = 0.6 * (o.offsetTop - c);
                const u = isInside(e, document.querySelector(".cta__bottom"), d);
                setTransform(e, "translateY(-" + d + "px)"),
                    u && $(".cta__links").addClass("anime"),
                    t > current
                        ? isInViewport(document.querySelector(".cta__bottom"), document.querySelector(".cta__bottom").getBoundingClientRect().bottom + 400) || $(".cta__links").removeClass("anime")
                        : isInViewport(document.querySelector(".cta__bottom"), document.querySelector(".cta__bottom").getBoundingClientRect().bottom) || $(".cta__links").removeClass("anime");
            } else new Flickity(e, { cellAlign: "left", freeScroll: !0, contain: !0, draggable: ">1", prevNextButtons: !1, pageDots: !1 });
            t = current;
        });
    },
    isInside = (e, t, o) => {
        var r = e.getBoundingClientRect(),
            i = t.getBoundingClientRect();
        return i.top <= r.top && r.top <= i.bottom && i.top <= r.bottom - o && r.bottom <= i.bottom && i.left <= r.left && r.left <= i.right && i.left <= r.right && r.right <= i.right;
    };
var header = document.querySelector(".topbar"),
    intro = document.querySelector(".home__intro"),
    logo = document.querySelector(".logo"),
    menuIcon = document.querySelector(".menubtn__icon"),
    menuBtn = document.querySelector(".menubtn"),
    drawer = document.querySelector(".drawer"),
    projects = document.querySelectorAll(".projects__item");
let newScrollPosition,
    oldScrollPosition = 0;
const goNextSlide = () => {
        var e = $(window).scrollTop() / $(window).height() + 0.01,
            t = document.querySelectorAll(".projects__item").length,
            o = Math.ceil(e) * $(window).height();
        Math.ceil(e) >= document.querySelectorAll(".projects__item").length || (o <= $(window).height() * t && $("html, body").stop().animate({ scrollTop: o }, 500, "swing"));
    },
    goPrevSlide = () => {
        var e = $(window).scrollTop() / $(window).height() - 0.01,
            t = Math.floor(e) * $(window).height();
        Math.round(e) - 1 < 0 || $("html, body").stop().animate({ scrollTop: t }, 500, "swing");
    },
    headerAnimation = () => {
        newScrollPosition = window.pageYOffset || document.documentElement.scrollTop;
        const e = document.querySelector(".home"),
            t = document.querySelector(".projects--slideview"),
            o = document.querySelector(".about"),
            r = () => oldScrollPosition - newScrollPosition < 0,
            i = () => oldScrollPosition - newScrollPosition > 0,
            s = () => {
                header.classList.add("hidden"), header.classList.remove("isBlur");
            },
            n = () => {
                header.classList.remove("hidden"), header.classList.add("isBlur");
            },
            c = () => {
                header.classList.remove("hidden"), header.classList.remove("isBlur"), header.classList.remove("noTransition");
            };
        e && (r() && !isInViewport(intro, 500) ? s() : i() && !isInViewport(intro, 0) ? n() : i() && isInViewport(intro, 0) ? (header.classList.remove("isBlur"), header.classList.add("noTransition")) : c()),
            t ? c() : addBlackBGHeader(),
            e || t || (r() ? s() : window.pageYOffset > 0 ? n() : c()),
            o && 0 == window.pageYOffset ? header.classList.add("alternate") : header.classList.remove("alternate"),
            document.querySelector(".drawer--active") && (header.classList.remove("hidden"), header.classList.remove("isBlack"), header.classList.remove("isDark")),
            (oldScrollPosition = newScrollPosition <= 0 ? 0 : newScrollPosition);
    },
    addBlackBGHeader = () => {
        const e = [...document.querySelectorAll(".background--dark"), ...document.querySelectorAll(".background--black"), ...document.querySelectorAll(".background--light"), ...document.querySelectorAll("section")],
            t = (e) => e.classList.contains("background--black"),
            o = (e) => e.classList.contains("background--dark");
        for (let i = 0; i < e.length; i++)
            isInViewport((r = e[i]), 0) &&
                window.pageYOffset + r.getBoundingClientRect().top <= window.pageYOffset &&
                (t(e[i])
                    ? (header.classList.add("isBlack"), header.classList.remove("isDark"))
                    : o(e[i])
                    ? (header.classList.add("isDark"), header.classList.remove("isBlack"))
                    : (header.classList.remove("isBlack"), header.classList.remove("isDark")));
        var r;
    },
    isInViewport = (e, t) => {
        var o = e.getBoundingClientRect();
        return o.bottom >= t && o.right >= 0 && o.top <= document.documentElement.clientHeight && o.left <= document.documentElement.clientWidth;
    };
var headerClasses;
const toggleMenu = () => {
        document.querySelector("body").classList.toggle("drawer--active");
        const e = document.querySelector(".topbar");
        document.querySelector("body").classList.contains("drawer--active")
            ? ((headerClasses = e.getAttribute("class").split(" ")),
              (menuBtn.querySelector(".menubtn__title").innerHTML = "Close"),
              e.classList.remove("isBlur"),
              e.classList.remove("hidden"),
              e.classList.remove("isBlack"),
              e.classList.remove("isDark"))
            : ((menuBtn.querySelector(".menubtn__title").innerHTML = "Menu"),
              headerClasses.forEach((t) => {
                  e.classList.add(t);
              }));
    },
    addRoute = (e) => {
        e.preventDefault();
        const t = e.currentTarget.href;
        if (document.querySelector("#projects-archive") && document.querySelector("#projects-archive").classList.contains("projects__slider")) {
            if (!(e.currentTarget.classList.contains("isSelected") || e.currentTarget.parentElement.classList.contains("menu-item") || e.currentTarget.parentElement.classList.contains("topbar__inner")))
                return void document.querySelectorAll(".projects__item").forEach((t) => {
                    const o = document.querySelector(".projects__item.isSelected");
                    [...document.querySelectorAll(".projects__item")].indexOf(o) > [...document.querySelectorAll(".projects__item")].indexOf(e.currentTarget) ? goPrevSlide() : goNextSlide(),
                        (document.querySelector(".totalProject").innerHTML = document.querySelectorAll(".projects__item").length);
                });
            (document.querySelector(".topbar").style.opacity = "0"),
                document.querySelector("#body").classList.add("clicked"),
                (e.currentTarget.style.zIndex = "999"),
                setTimeout(() => {
                    window.location = t;
                }, 1100);
        } else
            document.querySelector("#projects-archive") &&
                (document.querySelector("#body").classList.add("clicked"),
                (e.currentTarget.style.zIndex = "999"),
                setTimeout(() => {
                    window.location = t;
                }, 1100));
        t &&
            !e.currentTarget.classList.contains("smooth-scroll") &&
            ((document.querySelector(".topbar").style.opacity = "0"),
            document.querySelector("#body").classList.add("clicked"),
            (e.currentTarget.style.zIndex = "999"),
            setTimeout(() => {
                window.location = t;
            }, 1100));
    },
    moduleAnimation = (e) => {
        isInViewport(e, 0) && (e.style.animation = "fadeIn 1.3s cubic-bezier(0.61, 0.01, 0.09, 1.01) backwards"), (document.querySelector("footer").style.animation = "fadeIn 1.3s 0.5s cubic-bezier(0.61, 0.01, 0.09, 1.01) backwards");
    },
    effectElementsOnViewport = (e) => {
        [...e.children].forEach((e) => {
            document.querySelector(".projects") || document.querySelector(".project") || document.querySelector(".services") || document.querySelector(".about") || moduleAnimation(e),
                document.querySelector(".project__transform ") ||
                    document.querySelector(".services") ||
                    document.querySelector(".about") ||
                    [...e.children].forEach((e) => {
                        moduleAnimation(e);
                    });
        });
    };
window.addEventListener("DOMContentLoaded", () => {
    animeElementsOnViewport();
});
const animeElementsOnViewport = () => {
    let e = 0;
    document.querySelector(".home") || effectElementsOnViewport(document.querySelector("#body")),
        document.querySelector(".project") && effectElementsOnViewport(document.querySelector(".project__transform")),
        document.querySelector(".list__grid__item") &&
            isInViewport(document.querySelector(".list__grid__item"), 0) &&
            document.querySelectorAll(".list__grid__item").forEach((t) => {
                (t.style.animation = "fadeIn  1.3s cubic-bezier(0.61, 0.01, 0.09, 1.01) forwards"), (t.style.animationDelay = e / 10 + "s"), e++;
            });
};
let initialX = null,
    initialY = null;
const startTouch = (e) => {
        (initialX = e.touches[0].clientX), (initialY = e.touches[0].clientY);
    },
    goSliderForward = () => {
        var e = document.querySelectorAll(".selected-projects__slide").length,
            t = [...document.querySelectorAll(".selected-projects__slide")].find((e) => e.classList.contains("isSelected")),
            o = [...document.querySelectorAll(".selected-projects__slide")].indexOf(t),
            r = document.querySelector(".selected-projects__overlay .title"),
            i = document.querySelector(".selected-projects__overlay .subtitle"),
            s = 100 * (o + 1);
        o + 1 >= e ||
            ((document.querySelector(".selected-projects__slider").style.transform = `translateX(-${s}vw)`),
            document.querySelectorAll(".selected-projects__slide").forEach((e) => e.classList.remove("isSelected")),
            document.querySelectorAll(".selected-projects__slide")[o + 1].classList.add("isSelected"),
            (document.querySelector(".currentProject").innerHTML = Math.round(o + 1) + 1),
            (r.innerText = document.querySelectorAll(".selected-projects__slide")[o + 1].dataset.title),
            (i.innerText = document.querySelectorAll(".selected-projects__slide")[o + 1].dataset.subtitle));
    },
    goSliderBack = () => {
        document.querySelectorAll(".selected-projects__slide").length;
        var e = [...document.querySelectorAll(".selected-projects__slide")].find((e) => e.classList.contains("isSelected")),
            t = [...document.querySelectorAll(".selected-projects__slide")].indexOf(e),
            o = document.querySelector(".selected-projects__overlay .title"),
            r = document.querySelector(".selected-projects__overlay .subtitle"),
            i = 100 * (t - 1);
        t - 1 < 0 ||
            ((document.querySelector(".selected-projects__slider").style.transform = `translateX(-${i}vw)`),
            document.querySelectorAll(".selected-projects__slide").forEach((e) => e.classList.remove("isSelected")),
            document.querySelectorAll(".selected-projects__slide")[t - 1].classList.add("isSelected"),
            (document.querySelector(".currentProject").innerHTML = Math.round(t)),
            (o.innerText = document.querySelectorAll(".selected-projects__slide")[t - 1].dataset.title),
            (r.innerText = document.querySelectorAll(".selected-projects__slide")[t - 1].dataset.subtitle));
    },
    moveTouch = (e) => {
        if (null === initialX) return;
        if (null === initialY) return;
        let t = e.touches[0].clientX,
            o = e.touches[0].clientY,
            r = initialX - t,
            i = initialY - o;
        Math.abs(r) > Math.abs(i) && (r > 0 ? goSliderForward() : goSliderBack()), (initialX = null), (initialY = null), e.preventDefault();
    };
menuBtn.addEventListener("click", () => toggleMenu()), drawer.addEventListener("click", () => document.querySelector("body").classList.remove("drawer--active")), window.addEventListener("scroll", headerAnimation);
const linksNotEmail = [...document.querySelectorAll("a")].filter((e) => !e.href.includes("mailto") && !e.target);
linksNotEmail.forEach((e) => e.addEventListener("click", addRoute)),
    document.querySelector(".selected-projects") &&
        (document.querySelector(".selected-projects__arrow--next").addEventListener("click", goSliderForward), document.querySelector(".selected-projects__arrow--prev").addEventListener("click", goSliderBack)),
    document.querySelector("body").addEventListener(
        "touchstart",
        (e) => {
            e.target && e.target.closest(".selected-projects__slide") && startTouch(e);
        },
        { passive: !0 }
    ),
    document.querySelector("body").addEventListener(
        "touchmove",
        (e) => {
            e.target && e.target.closest(".selected-projects__slide") && moveTouch(e);
        },
        { passive: !0 }
    ),
    document.querySelectorAll(".list__grid__item").forEach((e) => {
        e.addEventListener("mouseenter", (t) => {
            (e.closest(".dropdown") || "A" == e.tagName) &&
                (e.classList.add("animated"),
                e.addEventListener("animationiteration", () => {
                    e.classList.remove("animated"), e.classList.add("animated");
                }));
        }),
            e.addEventListener("mouseleave", (t) => {
                (e.closest(".dropdown") || "A" == e.tagName) &&
                    e.addEventListener("animationiteration", () => {
                        e.classList.remove("animated");
                    });
            });
    }),
    document.querySelectorAll(".arrow").forEach((e) => {
        e.addEventListener("mouseenter", (t) => {
            e.classList.add("animated"),
                e.addEventListener("animationiteration", () => {
                    e.classList.remove("animated"), e.classList.add("animated");
                });
        }),
            e.addEventListener("mouseleave", (t) => {
                e.addEventListener("animationiteration", () => {
                    e.classList.remove("animated");
                });
            });
    }),
    jQuery(function (e) {
        e(".home__intro__blur").width();
        document.querySelector(".about") && header.classList.add("alternate");
        var t = 0,
            o = e(".home__fullvideo"),
            r = document.getElementById("video");
        if (r) var i = new Vimeo.Player(r);
        function s() {
            e(".topbar").css({ opacity: "0", visibility: "hidden" }),
                e("body").css({ overflow: "hidden" }),
                o.find(".home__fullvideo__close").css("opacity", 1),
                o.addClass("open"),
                setTimeout(() => {
                    i.play();
                }, 1400);
        }
        function n() {
            e(".topbar").css({ opacity: "", visibility: "" }), e("body").css({ overflow: "unset" }), o.removeClass("open"), o.find(".home__fullvideo__close").css("opacity", 0), i.pause();
        }
        e("body").on("mousemove", function (e) {
            t = e;
        }),
            e(".home__intro__video").each(function () {
                var t,
                    r,
                    i = e(".home__intro__btn"),
                    c = e(".home__fullvideo__close");
                e(this).css("cursor", "none"),
                    e(this).on("mouseenter", function (e) {
                        i.css("opacity", 1);
                    }),
                    e(this).on("mousemove", function (e) {
                        (t = e.clientX - 20), (r = e.clientY - 20);
                    }),
                    e(this).on("mouseleave", function (e) {
                        i.css("opacity", 0);
                    });
                const l = () => {
                    i.css({ transform: "translate(" + t + "px, " + r + "px)" }), requestAnimationFrame(l);
                };
                requestAnimationFrame(l),
                    e(this).on("click", function () {
                        s();
                    }),
                    o.on("click", function () {
                        n();
                    }),
                    c.on("click", function () {
                        n();
                    });
            }),
            e("#playIntroVideo").on("click", function () {
                s();
            }),
            e("#projects").each(function () {
                var o = e(this),
                    r = (o.offset().top, o.find(".selected-projects__slider").children()),
                    i = o.find(".title"),
                    s = o.find(".subtitle"),
                    n = (o.find(".scrollbar__fill"), o.find(".scrollbar__empty"), 100 * r.length);
                const c = document.querySelector(".selected-projects__overlay");
                c.getBoundingClientRect().right;
                if (
                    (o.find(".selected-projects__slider").width(n + "vw"),
                    r[0].classList.add("isSelected"),
                    i.html(r[0].dataset.title),
                    s.html(r[0].dataset.subtitle),
                    (c.querySelector(".currentProject").innerHTML = 1),
                    (c.querySelector(".totalProject").innerHTML = r.length),
                    window.innerWidth >= 768)
                ) {
                    o.find(".selected-projects__content").height(n + "vh"), r[0].classList.remove("isSelected");
                    o.outerHeight();
                    var l = e(".selected-projects__cursor");
                    e(".selected-projects__slide").css("cursor", "none"),
                        e(".selected-projects__inner").on("mouseover", function () {
                            l.css("opacity", 1);
                        }),
                        e(".selected-projects__inner").on("mouseleave", function () {
                            l.css("opacity", 0);
                        }),
                        e(".selected-projects__inner").on("mousemove", function () {
                            var e = t.clientX - 20,
                                o = t.clientY - 20;
                            l.css({ transform: "translate(" + e + "px, " + o + "px)" });
                        });
                }
            });
        let c = e(".projects__archive").height();
        e(window).scroll(function () {
            let t = e(window).scrollTop() / c;
            if (t <= 1) {
                var o = 0.02 + t,
                    r = 0.96 - t;
                e(".projects .scrollbar--vertical .scrollbar__fill").css("transform", "scaleX(" + o + ")"), e(".projects .scrollbar--vertical .scrollbar__empty").css("transform", "scaleX(" + r + ")");
            }
        });
        const l = (e, t) => {
            if (history.pushState) {
                let o = new URLSearchParams(window.location.search);
                o.set(e, t);
                let r = window.location.protocol + "//" + window.location.host + window.location.pathname + "?" + o.toString();
                window.history.pushState({ path: r }, "", r);
            }
        };
        e(document).ready(function () {
            let o = window.location.hash.replace(/^#/g, ""),
                r = "all";
            o && (r = '[data-cat~="' + o + '"]');
            var i = e("#filterCategory"),
                s = e(".projects--page"),
                n = e("#projects-archive"),
                a = e("#latest-archive"),
                d = e("#sort-select"),
                u = e(".toggle");
            const m = document.querySelector(".projects");
            function _(t) {
                s.find("#projects-archive");
                var a = s.find(".projects__item").length,
                    d = s.find(".projects__slider__arrow--next"),
                    _ = s.find(".projects__slider__arrow--prev");
                if ((e("html, body").stop().animate({ scrollTop: 0 }, 100, "swing"), "grid" == t)) {
                    const t = document.querySelector(".projects");
                    (t.querySelector(".content").style.opacity = 0),
                        (t.querySelector("#projects-archive").style.opacity = 0),
                        t.querySelector(".projects__slider__overlay") && (t.querySelector(".projects__slider__overlay").style.opacity = 0),
                        l("view", "grid"),
                        setTimeout(() => {
                            s.height(""),
                                t.querySelector(".projects__slider__toggle") && (t.querySelector(".projects__slider__toggle").style.opacity = 0),
                                n.removeClass("projects__slider"),
                                document.querySelector(".projects").classList.add("changeViewAnimation"),
                                (t.querySelector(".content").style.opacity = 1),
                                (document.querySelector(".hero__grid").style.opacity = 1),
                                t.querySelector(".projects__slider__toggle") && (t.querySelector(".projects__slider__toggle").style.opacity = 1),
                                t.querySelector(".projects__slider__overlay") && (t.querySelector(".projects__slider__overlay").style.opacity = 1),
                                n.addClass("projects__grid"),
                                (t.querySelector("#projects-archive").style.opacity = 1),
                                (t.querySelector("#projects-archive").style.transform = "none");
                            for (var l = 0; l < document.querySelectorAll(".projects__grid a").length - 1; l++) document.querySelectorAll(".projects__grid a")[l].style.animationDelay = l / 10 + "s";
                            t.querySelectorAll(".projects__item__content").forEach((e) => {
                                (e.style.backgroundColor = "rgba(255, 255, 255, 0.1)"), (e.style.backdropFilter = "blur(20px)"), (e.style.WebkitBackdropFilter = "blur(20px)");
                            }),
                                e("#body").removeClass("projects--slideview").addClass("projects--gridview"),
                                e(".projects__archive").addClass("background--black").removeClass("background--dark"),
                                e(".projects__item").removeAttr("style").find("img").removeAttr("style"),
                                e("#toggle__grid").addClass("active").siblings("label").removeClass("active"),
                                e("#toggle").prop("checked", !0),
                                u.appendTo(".hero__grid");
                            var a = mixitup(n, {
                                selectors: { target: ".projects__item" },
                                multifilter: { enable: !0 },
                                animation: { duration: 500 },
                                callbacks: {
                                    onMixStart: function (t, o) {
                                        !(function (t) {
                                            e.each(t, function (t, o) {
                                                t % 2 != 0 && window.innerWidth > 1024 ? e(o).css("top", "80px") : e(o).css("top", "0px");
                                            });
                                        })(o.show);
                                    },
                                    onMixEnd: function (t) {
                                        var o;
                                        (o = t.show),
                                            e(".projects__item").each(function (e, t) {
                                                o.forEach(function (e) {
                                                    t === e && d.push(t);
                                                });
                                            }),
                                            (c = e(".projects__archive").height());
                                    },
                                },
                            });
                            i.each(function () {
                                e(this).on("change", function () {
                                    a.setFilterGroupSelectors(this.name, this.value), a.parseFilterGroups();
                                }),
                                    o &&
                                        (a.setFilterGroupSelectors(this.name, r),
                                        setTimeout(function () {
                                            a.parseFilterGroups();
                                        }, 500)),
                                    e(this).select2({ minimumResultsForSearch: 1 / 0, width: "100%" });
                            });
                            var d = [];
                            e(".projects__item")
                                .on("mouseover", function () {
                                    e(".projects__grid .projects__item .projects__item__image").css({ opacity: "0.4" }), e(this).children(".projects__item__image").css({ opacity: 1 });
                                })
                                .on("mouseleave", function () {
                                    e(".projects__grid .projects__item .projects__item__image").css({ opacity: "1" });
                                });
                        }, 800);
                } else if ("slider" == t) {
                    e("#projects-archive")
                        .find(".projects__item")
                        .each(function (t) {
                            var o = e(this).find("img"),
                                r = e(this).index(),
                                i = -500 * (r + 0),
                                s = Math.abs((r + 0) / 3);
                            (s = Math.max(1, Math.min(1.5, s + 1))), o.css({ transform: "translateX( " + i + "px) scale(" + s + ")" });
                        }),
                        (m.querySelector(".content").style.opacity = 0),
                        (m.querySelector("#projects-archive").style.opacity = 0),
                        (document.querySelector(".hero__grid").style.opacity = 0),
                        l("view", "slider"),
                        setTimeout(() => {
                            n.removeClass("projects__grid"),
                                document.querySelector(".projects").classList.add("changeViewAnimation"),
                                (m.querySelector(".content").style.opacity = 1),
                                (m.querySelector("#projects-archive").style.opacity = 1),
                                n.addClass("projects__slider"),
                                e("#body").addClass("projects--slideview").removeClass("projects--gridview"),
                                e(".projects__archive").removeClass("background--black").addClass("background--dark"),
                                e(".projects__item").removeAttr("style").find("img"),
                                e("#toggle__slider").addClass("active").siblings("label").removeClass("active"),
                                u.appendTo(".projects__slider__toggle"),
                                s.height(100 * a + "vh"),
                                document.querySelector(".topbar").classList.remove("isBlack");
                        }, 800),
                        _.on("click", function (e) {
                            goPrevSlide();
                        }),
                        d.on("click", function (e) {
                            goNextSlide();
                        }),
                        (document.querySelector(".currentProject").innerHTML = Math.ceil(0) + 1),
                        (document.querySelector(".totalProject").innerHTML = document.querySelectorAll(".projects__item").length);
                }
            }
            s.length && (document.location.search.includes("grid") || o ? _("grid") : _("slider"), window.innerWidth <= 1024 && _("grid"), document.querySelectorAll(".projects__item")[0].classList.add("isSelected")),
                document.querySelector("#body").classList.contains("projects--gridview") && _("grid");
            var h = e(".projects__cursor");
            e(".projects__item").css("cursor", "none"),
                e(".projects__item").on("mouseover", function () {
                    h.css("opacity", 1);
                }),
                e(".projects__item").on("mouseleave", function () {
                    h.css("opacity", 0);
                }),
                e(".projects__item").on("mousemove", function () {
                    var e = t.clientX - 20,
                        o = t.clientY - 20;
                    h.css({ transform: "translate(" + e + "px, " + o + "px)" });
                }),
                e("#toggle").change(function () {
                    n.hasClass("projects__slider") ? _("grid") : _("slider");
                }),
                a.each(function () {
                    var t = mixitup(a, { selectors: { target: ".latest__item" }, multifilter: { enable: !0 }, animation: { duration: 500 } });
                    d.on("change", function () {
                        t.sort(this.value);
                    }),
                        d.select2({ minimumResultsForSearch: 1 / 0, width: "100%" }),
                        a.find(".latest__item").each(function () {
                            e(this)
                                .on("mouseover", function () {
                                    a.find(".latest__item").css({ opacity: "0.4" }), e(this).css({ opacity: 1 });
                                })
                                .on("mouseleave", function () {
                                    a.find(".latest__item").css({ opacity: "1" });
                                });
                        });
                });
        }),
            e(document).ready(function () {
                let t = window.location.hash;
                t &&
                    e("html, body")
                        .stop()
                        .animate({ scrollTop: e(t).offset().top }, 1e3, "swing"),
                    e(".smooth-scroll").on("click", function (t) {
                        if ("" !== this.hash) {
                            t.preventDefault();
                            let o = this.hash;
                            e("html, body")
                                .stop()
                                .animate({ scrollTop: e(o).offset().top }, 1e3, "swing");
                        }
                    });
            }),
            e(window).on("resize", function () {});
        (() => {
            const e = document.querySelectorAll(".workflow__bullet-lines__outer-circle");
            e.length &&
                ([...e].forEach((e) => {
                    const t = 2 * e.r.baseVal.value * Math.PI;
                    (e.style.strokeDasharray = `${t} ${t}`), (e.style.strokeDashoffset = "" + t);
                }),
                (document.querySelectorAll(".workflow .line")[document.querySelectorAll(".workflow .line").length - 1].style.display = "none"));
        })(),
            e(window).on("scroll load", function () {
                let t = e(window).scrollTop();
                e(window).width() >= 768 &&
                    e(".service__item").each(function (o, r) {
                        let i = e(".service__list").children(".service__list__item").eq(o),
                            s = e(this).height() + e(this).offset().top,
                            n = (t - e(this).offset().top) / e(this).height();
                        t > e(this).offset().top &&
                            t < s &&
                            (i.addClass("active").siblings().removeClass("active"),
                            i.children(".service__list__navbar").addClass("active").slideDown(),
                            i.siblings().children(".service__list__navbar").removeClass("active").slideUp(),
                            i.find(".service__list__navbar--progress-bar--increment").css("transform", "scaleY(" + n + ")"));
                    });
            });
        let a = e("#hero").outerHeight();
        e(window).on("scroll", () => {
            let t = e(window).scrollTop() / a,
                o = Math.min(Math.max(t, 0), 1),
                r = 0.02 + o,
                i = 0.96 - o;
            e(".services .scrollbar__fill").css("transform", "scaleX(" + r + ")"), e(".services .scrollbar__empty").css("transform", "scaleX(" + i + ")");
            let s = 0;
            [...document.querySelectorAll(".workflow__bullet-lines")].forEach((e) => {
                isInViewport(e, 100) &&
                    ((e.querySelector(".workflow__bullet-lines__outer-circle").style.transition = `stroke-dashoffset 0.6s ${s}s ease`),
                    (e.querySelector(".workflow__bullet-lines__outer-circle").style.strokeDashoffset = "0"),
                    e.querySelector(".workflow__bullet-lines__outer-circle").addEventListener("transitionend", () => {
                        (e.querySelector(".line").style.transition = "height 0.8s ease"),
                            (e.querySelector(".line").style.height = "calc(100% - 20px)"),
                            (e.nextElementSibling.querySelector("h3").style.animation = "fadeIn 0.8s ease forwards"),
                            (e.nextElementSibling.querySelector("p").style.animation = "fadeIn 0.8s 0.2s ease forwards");
                    }),
                    (s += 0.8));
            });
        });
        var d = document.querySelector(".related__slider");
        if (
            (d &&
                (function (e) {
                    var t = e.querySelector(".related__carousel");
                    document.querySelectorAll(".single-article");
                    if (t) {
                        t.style.display = "block";
                        var o = new Flickity(t, {
                            contain: !0,
                            cellAlign: "left",
                            wrapAround: !1,
                            draggable: !0,
                            prevNextButtons: !1,
                            pageDots: !1,
                            imagesLoaded: !0,
                            lazyLoad: 3,
                            on: {
                                ready: function () {
                                    t.style.opacity = 1;
                                },
                            },
                        });
                    }
                    var r = document.querySelector(".related__btn--prev");
                    r &&
                        r.addEventListener("click", function () {
                            o.previous();
                        });
                    var i = document.querySelector(".related__btn--next");
                    i &&
                        i.addEventListener("click", function () {
                            o.next();
                        });
                    var s = document.querySelectorAll(".single-article__link");
                    s.forEach(function (e) {
                        e.addEventListener("mouseenter", function () {
                            s.forEach(function (e) {
                                e.querySelector(".single-article__image").style.opacity = 0.6;
                            }),
                                (this.querySelector(".single-article__image").style.opacity = 1),
                                (this.parentElement.style.zIndex = 9);
                        }),
                            e.addEventListener("mouseleave", function () {
                                (this.parentElement.style.zIndex = ""),
                                    s.forEach(function (e) {
                                        e.querySelector(".single-article__image").style.opacity = 1;
                                    });
                            });
                    });
                })(d),
            e(window).width() < 768)
        ) {
            var u = document.querySelector(".leadership__slider");
            u &&
                (function (e) {
                    var t = e.querySelector(".leadership__carousel");
                    if (t) {
                        t.style.display = "block";
                        var o = new Flickity(t, {
                            cellAlign: "left",
                            draggable: !0,
                            prevNextButtons: !1,
                            freeScroll: !1,
                            pageDots: !1,
                            on: {
                                ready: function () {
                                    t.style.opacity = 1;
                                },
                            },
                        });
                    }
                    var r = document.querySelector(".leadership__btn--prev");
                    r &&
                        r.addEventListener("click", function () {
                            o.previous();
                        });
                    var i = document.querySelector(".leadership__btn--next");
                    i &&
                        i.addEventListener("click", function () {
                            o.next();
                        });
                })(u);
        }
        let m,
            _ = e("#hero").outerHeight();
        e(window).scroll(function () {
            let t = e(window).scrollTop() / _,
                o = Math.min(Math.max(t, 0), 1),
                r = 0.02 + o,
                i = 0.96 - o;
            e(".about .scrollbar__fill").css("transform", "scaleX(" + r + ")"), e(".about .scrollbar__empty").css("transform", "scaleX(" + i + ")");
        });
        const h = () => {
                document.querySelectorAll(".image-slider").forEach((e) => {
                    const t = e.offsetTop;
                    e.querySelectorAll(".garage-door__image").forEach((e) => {
                        const o = e,
                            r = o.querySelector("img"),
                            i = document.querySelectorAll(".image-slider__pagination__slide"),
                            s = parseInt(o.dataset.id);
                        let n = o.clientHeight,
                            c = s >= 1 ? t + n * (s - 1) : t,
                            l = window.pageYOffset,
                            a = 0 == s ? l / (c + n - window.innerHeight) : (l - (c + n - window.innerHeight)) / n,
                            d = Math.min(Math.max(a, 0), 1);
                        if ((s > 0 && (r.style.opacity = d), 0 == s)) {
                            p(d < 1 && 0 != d, i[s], d);
                        } else if (s >= i[i.length - 1].dataset.id) {
                            p(d > 0, i[s], d);
                        } else {
                            p(d > 0 && d < 1, i[s], d);
                        }
                    });
                });
            },
            y = (e, t, o) => {
                const r = o - t * o;
                e.style.strokeDashoffset = r;
            },
            p = (e, t, o) => {
                e ? (t.classList.add("active"), (m = o)) : t.classList.remove("active");
            };
        document.querySelectorAll(".progress-ring__circle");
        e(window).on("load", function () {
            h(),
                document.querySelectorAll(".progress-ring__circle").forEach((e) => {
                    const t = 2 * e.r.baseVal.value * Math.PI;
                    (e.style.strokeDasharray = `${t} ${t}`), (e.style.strokeDashoffset = "" + t), y(e, m, t);
                });
        }),
            window.addEventListener("scroll", function () {
                h(),
                    document.querySelectorAll(".progress-ring__circle").forEach((e) => {
                        const t = 2 * e.r.baseVal.value * Math.PI;
                        y(e, m, t);
                    });
            }),
            e(".video__play").on("click", function () {
                e(this).siblings(".video__full").addClass("open").fadeIn(300).children("video").get(0).play(), e(".topbar").css({ opacity: "0", visibility: "hidden" }), e("body").css({ overflow: "hidden" });
            }),
            e(".video__full").on("click", function (t) {
                var o = e(this).children("video").get(0);
                o.pause(), (o.currentTime = 0), e(this).removeClass("open"), e(".topbar").css({ opacity: "1", visibility: "visible" }), e("body").css({ overflow: "unset" });
            }),
            e(".fullVideo").on("click", function (t) {
                t.stopPropagation();
                var o = e(this).get(0);
                o.paused ? o.play() : o.pause();
            }),
            e(".video__play").each(function () {
                var o = e(".video__btn");
                e("html").hasClass("no-touchevents") &&
                    (e(this).css("cursor", "none"),
                    e(this).on("mouseover", function () {
                        o.css("opacity", 1);
                    }),
                    e(this).on("mouseleave", function () {
                        o.css("opacity", 0);
                    }),
                    e(this).on("mousemove", function () {
                        var e = t.clientX - 20,
                            r = t.clientY - 20;
                        o.css({ transform: "translate(" + e + "px, " + r + "px)" });
                    }));
            }),
            e(".next-project__full--anchor").each(function () {
                var o = e(".btn__view");
                e("html").hasClass("no-touchevents") &&
                    (e(this).css("cursor", "none"),
                    e(this).on("mouseover", function () {
                        o.css("opacity", 1);
                    }),
                    e(this).on("mouseleave", function () {
                        o.css("opacity", 0);
                    }),
                    e(this).on("mousemove", function () {
                        var e = t.clientX - 20,
                            r = t.clientY - 20;
                        o.css({ transform: "translate(" + e + "px, " + r + "px)" });
                    }));
            });
        let f = e("#archiveFilter");
        f.select2({ minimumResultsForSearch: 1 / 0, width: "100%" }),
            f.on("change", function () {
                window.location = init.home_url + "/archive/" + this.value;
            }),
            e("#drop-down .list__grid__item").on("click", function () {
                e(this).toggleClass("list__grid__item--open");
                var t = e(this).find(".list__grid__text").stop(!0);
                e(this).hasClass("list__grid__item--open") ? t.animate({ height: t.prop("scrollHeight") }, 500) : t.animate({ height: 0 }, 500);
            });
        const v = document.querySelector(".hero__categories ul");
        if (v)
            new Flickity(v, {
                contain: !1,
                cellAlign: "left",
                wrapAround: !1,
                draggable: !0,
                prevNextButtons: !1,
                pageDots: !1,
                watchCSS: !0,
                on: {
                    ready: function () {
                        v.style.opacity = 1;
                    },
                },
            });
    });
