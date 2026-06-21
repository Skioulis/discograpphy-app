/* @ds-bundle: {"format":3,"namespace":"SakisCollectionDesignSystem_2efc19","components":[{"name":"DiskCard","sourcePath":"components/collection/DiskCard.jsx"},{"name":"GREEK_LETTERS","sourcePath":"components/collection/GreekAlphabetFilter.jsx"},{"name":"GreekAlphabetFilter","sourcePath":"components/collection/GreekAlphabetFilter.jsx"},{"name":"SongCard","sourcePath":"components/collection/SongCard.jsx"},{"name":"Badge","sourcePath":"components/core/Badge.jsx"},{"name":"Button","sourcePath":"components/core/Button.jsx"},{"name":"Card","sourcePath":"components/core/Card.jsx"},{"name":"Input","sourcePath":"components/forms/Input.jsx"},{"name":"Select","sourcePath":"components/forms/Select.jsx"},{"name":"Navbar","sourcePath":"components/navigation/Navbar.jsx"},{"name":"Pagination","sourcePath":"components/navigation/Pagination.jsx"}],"sourceHashes":{"components/collection/DiskCard.jsx":"019f3963ad22","components/collection/GreekAlphabetFilter.jsx":"b540108b7b0a","components/collection/SongCard.jsx":"4e448581f25d","components/core/Badge.jsx":"6618ceb7db94","components/core/Button.jsx":"7b4be8430f73","components/core/Card.jsx":"3632930e715d","components/forms/Input.jsx":"38ffcc54f321","components/forms/Select.jsx":"a5489c44973d","components/navigation/Navbar.jsx":"08022069bcd4","components/navigation/Pagination.jsx":"77d4f37ce0de","ui_kits/sakis-collection/App.jsx":"ca0ccfce4255","ui_kits/sakis-collection/data.js":"4390644d7cd6"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.SakisCollectionDesignSystem_2efc19 = window.SakisCollectionDesignSystem_2efc19 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/collection/GreekAlphabetFilter.jsx
try { (() => {
/** The 24 letters of the Greek alphabet, in order. */
const GREEK_LETTERS = ['Α', 'Β', 'Γ', 'Δ', 'Ε', 'Ζ', 'Η', 'Θ', 'Ι', 'Κ', 'Λ', 'Μ', 'Ν', 'Ξ', 'Ο', 'Π', 'Ρ', 'Σ', 'Τ', 'Υ', 'Φ', 'Χ', 'Ψ', 'Ω'];

/**
 * Sakis Collection — GreekAlphabetFilter
 * A row of pill chips, one per Greek letter, for filtering a
 * catalogue (songs / disks) by its first letter. Includes an
 * "Όλα" (All) chip and an optional "#" chip for non-Greek/other.
 *
 * `available` (a Set/array of letters that have entries) dims and
 * disables the rest, so users only click letters that lead somewhere.
 */
function GreekAlphabetFilter({
  active = 'Όλα',
  onSelect,
  available = null,
  showAll = true,
  showOther = true,
  size = 'md',
  style = {}
}) {
  const avail = available == null ? null : new Set(available);
  const sizes = {
    sm: {
      dim: 30,
      font: 'var(--text-sm)'
    },
    md: {
      dim: 38,
      font: 'var(--text-md)'
    },
    lg: {
      dim: 46,
      font: 'var(--text-lg)'
    }
  };
  const S = sizes[size];
  const chips = [];
  if (showAll) chips.push({
    key: 'Όλα',
    label: 'Όλα',
    isAll: true
  });
  GREEK_LETTERS.forEach(l => chips.push({
    key: l,
    label: l
  }));
  if (showOther) chips.push({
    key: '#',
    label: '#'
  });
  return /*#__PURE__*/React.createElement("div", {
    role: "group",
    "aria-label": "\u03A6\u03AF\u03BB\u03C4\u03C1\u03BF \u03B5\u03BB\u03BB\u03B7\u03BD\u03B9\u03BA\u03BF\u03CD \u03B1\u03BB\u03C6\u03B1\u03B2\u03AE\u03C4\u03BF\u03C5",
    style: {
      display: 'flex',
      flexWrap: 'wrap',
      gap: '6px',
      ...style
    }
  }, chips.map(({
    key,
    label,
    isAll
  }) => {
    const isActive = active === key;
    const disabled = !isAll && key !== '#' && avail != null && !avail.has(key);
    return /*#__PURE__*/React.createElement("button", {
      key: key,
      type: "button",
      disabled: disabled,
      "aria-pressed": isActive,
      onClick: () => !disabled && onSelect && onSelect(key),
      style: {
        minWidth: isAll ? 'auto' : `${S.dim}px`,
        height: `${S.dim}px`,
        padding: isAll ? '0 16px' : '0',
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: 'var(--font-display)',
        fontSize: S.font,
        fontWeight: 'var(--weight-bold)',
        lineHeight: 1,
        color: isActive ? 'var(--paper-50)' : disabled ? 'var(--ink-300)' : 'var(--ink-700)',
        background: isActive ? 'var(--ink-900)' : disabled ? 'transparent' : 'var(--surface-raised)',
        border: `1px solid ${isActive ? 'var(--ink-900)' : 'var(--border-medium)'}`,
        borderRadius: 'var(--radius-pill)',
        boxShadow: isActive ? 'var(--shadow-sm)' : 'none',
        cursor: disabled ? 'default' : 'pointer',
        opacity: disabled ? 0.5 : 1,
        transition: 'all var(--duration-fast) var(--ease-standard)'
      },
      onMouseEnter: e => {
        if (disabled || isActive) return;
        e.currentTarget.style.background = 'var(--sage-300)';
        e.currentTarget.style.borderColor = 'var(--sage-500)';
      },
      onMouseLeave: e => {
        if (disabled || isActive) return;
        e.currentTarget.style.background = 'var(--surface-raised)';
        e.currentTarget.style.borderColor = 'var(--border-medium)';
      }
    }, label);
  }));
}
Object.assign(__ds_scope, { GREEK_LETTERS, GreekAlphabetFilter });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/collection/GreekAlphabetFilter.jsx", error: String((e && e.message) || e) }); }

// components/core/Badge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Sakis Collection — Badge
 * Small rounded count / status pill.
 */
function Badge({
  children,
  variant = 'neutral',
  style = {},
  ...rest
}) {
  const variants = {
    neutral: {
      background: 'var(--sage-200)',
      color: 'var(--ink-700)'
    },
    sage: {
      background: 'var(--sage-400)',
      color: 'var(--ink-900)'
    },
    rose: {
      background: 'var(--rose-300)',
      color: 'var(--ink-900)'
    },
    count: {
      background: 'var(--ink-900)',
      color: 'var(--paper-50)'
    },
    outline: {
      background: 'transparent',
      color: 'var(--ink-700)',
      boxShadow: 'inset 0 0 0 1px var(--border-medium)'
    }
  };
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '5px',
      minWidth: '22px',
      padding: '2px 10px',
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-xs)',
      fontWeight: 'var(--weight-bold)',
      letterSpacing: 'var(--tracking-wide)',
      lineHeight: 1.5,
      borderRadius: 'var(--radius-pill)',
      ...variants[variant],
      ...style
    }
  }, rest), children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Badge.jsx", error: String((e && e.message) || e) }); }

// components/core/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Sakis Collection — Button
 * Soft, friendly buttons in the brand's vintage palette.
 */
function Button({
  children,
  variant = 'primary',
  size = 'md',
  iconLeft = null,
  iconRight = null,
  disabled = false,
  type = 'button',
  onClick,
  style = {},
  ...rest
}) {
  const sizes = {
    sm: {
      padding: '6px 14px',
      fontSize: 'var(--text-sm)',
      gap: '6px'
    },
    md: {
      padding: '10px 20px',
      fontSize: 'var(--text-base)',
      gap: '8px'
    },
    lg: {
      padding: '14px 28px',
      fontSize: 'var(--text-md)',
      gap: '10px'
    }
  };
  const variants = {
    primary: {
      background: 'var(--rose-300)',
      color: 'var(--ink-900)',
      border: '1px solid var(--rose-400)'
    },
    secondary: {
      background: 'var(--sage-400)',
      color: 'var(--ink-900)',
      border: '1px solid var(--sage-500)'
    },
    outline: {
      background: 'transparent',
      color: 'var(--rose-500)',
      border: '1px solid var(--rose-400)'
    },
    ghost: {
      background: 'transparent',
      color: 'var(--ink-700)',
      border: '1px solid transparent'
    },
    danger: {
      background: 'transparent',
      color: 'var(--status-danger)',
      border: '1px solid var(--status-danger)'
    }
  };
  return /*#__PURE__*/React.createElement("button", _extends({
    type: type,
    disabled: disabled,
    onClick: onClick,
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: sizes[size].gap,
      padding: sizes[size].padding,
      fontSize: sizes[size].fontSize,
      fontFamily: 'var(--font-body)',
      fontWeight: 'var(--weight-bold)',
      lineHeight: 1,
      borderRadius: 'var(--radius-pill)',
      cursor: disabled ? 'not-allowed' : 'pointer',
      opacity: disabled ? 0.5 : 1,
      transition: 'transform var(--duration-fast) var(--ease-standard), filter var(--duration-fast) var(--ease-standard), box-shadow var(--duration-fast) var(--ease-standard)',
      boxShadow: 'var(--shadow-xs)',
      ...variants[variant],
      ...style
    },
    onMouseDown: e => {
      if (!disabled) e.currentTarget.style.transform = 'scale(0.96)';
    },
    onMouseUp: e => {
      e.currentTarget.style.transform = 'scale(1)';
    },
    onMouseEnter: e => {
      if (!disabled) e.currentTarget.style.filter = 'brightness(0.95)';
    },
    onMouseLeave: e => {
      e.currentTarget.style.filter = 'none';
      e.currentTarget.style.transform = 'scale(1)';
    }
  }, rest), iconLeft && /*#__PURE__*/React.createElement("span", {
    "aria-hidden": "true",
    style: {
      display: 'inline-flex'
    }
  }, iconLeft), children, iconRight && /*#__PURE__*/React.createElement("span", {
    "aria-hidden": "true",
    style: {
      display: 'inline-flex'
    }
  }, iconRight));
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Button.jsx", error: String((e && e.message) || e) }); }

// components/collection/DiskCard.jsx
try { (() => {
/**
 * Sakis Collection — DiskCard
 * A record/disk with company, size, catalogue id (sakisid) and song count.
 */
function DiskCard({
  name = '',
  company = '',
  size = null,
  sakisid = '',
  songCount = null,
  notes = '',
  onView,
  onEdit,
  onDelete,
  style = {}
}) {
  return /*#__PURE__*/React.createElement("article", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      background: 'var(--surface-raised)',
      border: '1px solid var(--border-soft)',
      borderRadius: 'var(--radius-md)',
      boxShadow: 'var(--shadow-sm)',
      overflow: 'hidden',
      transition: 'transform var(--duration-base) var(--ease-out), box-shadow var(--duration-base) var(--ease-out)',
      ...style
    },
    onMouseEnter: e => {
      e.currentTarget.style.transform = 'translateY(-3px)';
      e.currentTarget.style.boxShadow = 'var(--shadow-md)';
    },
    onMouseLeave: e => {
      e.currentTarget.style.transform = 'none';
      e.currentTarget.style.boxShadow = 'var(--shadow-sm)';
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: 'var(--space-5)',
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'flex-start',
      justifyContent: 'space-between',
      gap: '10px'
    }
  }, /*#__PURE__*/React.createElement("h3", {
    style: {
      margin: '0 0 4px',
      fontFamily: 'var(--font-display)',
      fontSize: 'var(--text-lg)',
      fontWeight: 'var(--weight-bold)',
      color: 'var(--rose-500)',
      lineHeight: 'var(--leading-snug)'
    }
  }, name), songCount != null && /*#__PURE__*/React.createElement(__ds_scope.Badge, {
    variant: "count"
  }, songCount)), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: '0 0 10px',
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-sm)',
      color: 'var(--ink-500)'
    }
  }, company || 'Χωρίς εταιρεία', size ? ` · ${size}″` : ''), sakisid && /*#__PURE__*/React.createElement("p", {
    style: {
      margin: '0 0 6px',
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--text-xs)',
      color: 'var(--ink-500)',
      letterSpacing: 'var(--tracking-wide)'
    }
  }, "ID: ", sakisid), notes && /*#__PURE__*/React.createElement("p", {
    style: {
      margin: '6px 0 0',
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-sm)',
      color: 'var(--ink-500)',
      whiteSpace: 'nowrap',
      overflow: 'hidden',
      textOverflow: 'ellipsis'
    }
  }, notes)), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      padding: 'var(--space-3) var(--space-5) var(--space-5)'
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.Button, {
    variant: "outline",
    size: "sm",
    onClick: onView
  }, "\u03A0\u03C1\u03BF\u03B2\u03BF\u03BB\u03AE"), /*#__PURE__*/React.createElement(__ds_scope.Button, {
    variant: "ghost",
    size: "sm",
    onClick: onEdit
  }, "\u0395\u03C0\u03B5\u03BE\u03B5\u03C1\u03B3\u03B1\u03C3\u03AF\u03B1"), /*#__PURE__*/React.createElement(__ds_scope.Button, {
    variant: "danger",
    size: "sm",
    onClick: onDelete,
    style: {
      marginLeft: 'auto'
    }
  }, "\u0394\u03B9\u03B1\u03B3\u03C1\u03B1\u03C6\u03AE")));
}
Object.assign(__ds_scope, { DiskCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/collection/DiskCard.jsx", error: String((e && e.message) || e) }); }

// components/collection/SongCard.jsx
try { (() => {
/**
 * Sakis Collection — SongCard
 * A song with its contributors (Συντελεστές) and roles. Mirrors the
 * original app's song card, restyled on the design-system tokens.
 */
function SongCard({
  title = '',
  contributors = [],
  notes = '',
  onView,
  onEdit,
  onDelete,
  style = {}
}) {
  return /*#__PURE__*/React.createElement("article", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      background: 'var(--surface-raised)',
      border: '1px solid var(--border-soft)',
      borderRadius: 'var(--radius-md)',
      boxShadow: 'var(--shadow-sm)',
      overflow: 'hidden',
      transition: 'transform var(--duration-base) var(--ease-out), box-shadow var(--duration-base) var(--ease-out)',
      ...style
    },
    onMouseEnter: e => {
      e.currentTarget.style.transform = 'translateY(-3px)';
      e.currentTarget.style.boxShadow = 'var(--shadow-md)';
    },
    onMouseLeave: e => {
      e.currentTarget.style.transform = 'none';
      e.currentTarget.style.boxShadow = 'var(--shadow-sm)';
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: 'var(--space-5)',
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("h3", {
    style: {
      margin: '0 0 4px',
      fontFamily: 'var(--font-display)',
      fontSize: 'var(--text-lg)',
      fontWeight: 'var(--weight-bold)',
      color: 'var(--rose-500)',
      lineHeight: 'var(--leading-snug)'
    }
  }, title), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: '0 0 10px',
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-xs)',
      fontWeight: 'var(--weight-bold)',
      letterSpacing: 'var(--tracking-caps)',
      textTransform: 'uppercase',
      color: 'var(--ink-500)'
    }
  }, "\u03A3\u03C5\u03BD\u03C4\u03B5\u03BB\u03B5\u03C3\u03C4\u03AD\u03C2"), /*#__PURE__*/React.createElement("ul", {
    style: {
      margin: 0,
      padding: 0,
      listStyle: 'none',
      display: 'flex',
      flexDirection: 'column',
      gap: '3px'
    }
  }, contributors.length === 0 && /*#__PURE__*/React.createElement("li", {
    style: {
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-sm)',
      color: 'var(--ink-500)',
      fontStyle: 'italic'
    }
  }, "\u0386\u03B3\u03BD\u03C9\u03C3\u03C4\u03BF\u03C2 \u03BA\u03B1\u03BB\u03BB\u03B9\u03C4\u03AD\u03C7\u03BD\u03B7\u03C2"), contributors.map((c, i) => /*#__PURE__*/React.createElement("li", {
    key: i,
    style: {
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-sm)',
      color: 'var(--ink-700)'
    }
  }, /*#__PURE__*/React.createElement("strong", {
    style: {
      fontWeight: 'var(--weight-bold)',
      color: 'var(--ink-900)'
    }
  }, c.name), c.roles && c.roles.length > 0 && /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--ink-500)'
    }
  }, " \xB7 ", c.roles.join(', '))))), notes && /*#__PURE__*/React.createElement("p", {
    style: {
      margin: '10px 0 0',
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-sm)',
      color: 'var(--ink-500)',
      whiteSpace: 'nowrap',
      overflow: 'hidden',
      textOverflow: 'ellipsis'
    }
  }, notes)), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      padding: 'var(--space-3) var(--space-5) var(--space-5)'
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.Button, {
    variant: "outline",
    size: "sm",
    onClick: onView
  }, "\u03A0\u03C1\u03BF\u03B2\u03BF\u03BB\u03AE"), /*#__PURE__*/React.createElement(__ds_scope.Button, {
    variant: "ghost",
    size: "sm",
    onClick: onEdit
  }, "\u0395\u03C0\u03B5\u03BE\u03B5\u03C1\u03B3\u03B1\u03C3\u03AF\u03B1"), /*#__PURE__*/React.createElement(__ds_scope.Button, {
    variant: "danger",
    size: "sm",
    onClick: onDelete,
    style: {
      marginLeft: 'auto'
    }
  }, "\u0394\u03B9\u03B1\u03B3\u03C1\u03B1\u03C6\u03AE")));
}
Object.assign(__ds_scope, { SongCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/collection/SongCard.jsx", error: String((e && e.message) || e) }); }

// components/core/Card.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Sakis Collection — Card
 * Paper-raised surface with soft rounding and a gentle shadow.
 */
function Card({
  children,
  interactive = false,
  padding = 'var(--space-5)',
  style = {},
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      background: 'var(--surface-raised)',
      borderRadius: 'var(--radius-md)',
      boxShadow: 'var(--shadow-sm)',
      border: '1px solid var(--border-soft)',
      padding,
      transition: 'transform var(--duration-base) var(--ease-out), box-shadow var(--duration-base) var(--ease-out)',
      ...style
    },
    onMouseEnter: interactive ? e => {
      e.currentTarget.style.transform = 'translateY(-3px)';
      e.currentTarget.style.boxShadow = 'var(--shadow-md)';
    } : undefined,
    onMouseLeave: interactive ? e => {
      e.currentTarget.style.transform = 'none';
      e.currentTarget.style.boxShadow = 'var(--shadow-sm)';
    } : undefined
  }, rest), children);
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Card.jsx", error: String((e && e.message) || e) }); }

// components/forms/Input.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Sakis Collection — Input
 * Text / search field. Pass icon for a leading glyph (e.g. search).
 */
function Input({
  type = 'text',
  placeholder = '',
  value,
  defaultValue,
  onChange,
  icon = null,
  label = null,
  id,
  disabled = false,
  style = {},
  ...rest
}) {
  const field = /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative',
      display: 'flex',
      alignItems: 'center'
    }
  }, icon && /*#__PURE__*/React.createElement("span", {
    "aria-hidden": "true",
    style: {
      position: 'absolute',
      left: '14px',
      display: 'inline-flex',
      color: 'var(--ink-500)',
      pointerEvents: 'none',
      fontSize: 'var(--text-base)'
    }
  }, icon), /*#__PURE__*/React.createElement("input", _extends({
    id: id,
    type: type,
    placeholder: placeholder,
    value: value,
    defaultValue: defaultValue,
    onChange: onChange,
    disabled: disabled,
    style: {
      width: '100%',
      padding: icon ? '10px 16px 10px 40px' : '10px 16px',
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-base)',
      color: 'var(--ink-900)',
      background: 'var(--surface-raised)',
      border: '1px solid var(--border-medium)',
      borderRadius: 'var(--radius-pill)',
      outline: 'none',
      boxShadow: 'var(--shadow-xs)',
      transition: 'border-color var(--duration-fast) var(--ease-standard), box-shadow var(--duration-fast) var(--ease-standard)',
      ...style
    },
    onFocus: e => {
      e.currentTarget.style.borderColor = 'var(--sage-500)';
      e.currentTarget.style.boxShadow = '0 0 0 3px rgba(126,147,141,0.25)';
    },
    onBlur: e => {
      e.currentTarget.style.borderColor = 'var(--border-medium)';
      e.currentTarget.style.boxShadow = 'var(--shadow-xs)';
    }
  }, rest)));
  if (!label) return field;
  return /*#__PURE__*/React.createElement("label", {
    htmlFor: id,
    style: {
      display: 'block'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'block',
      marginBottom: '6px',
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-sm)',
      fontWeight: 'var(--weight-bold)',
      color: 'var(--ink-700)'
    }
  }, label), field);
}
Object.assign(__ds_scope, { Input });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Input.jsx", error: String((e && e.message) || e) }); }

// components/forms/Select.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Sakis Collection — Select
 * Styled native dropdown (used for sort / per-page / search category).
 */
function Select({
  options = [],
  value,
  defaultValue,
  onChange,
  label = null,
  id,
  disabled = false,
  style = {},
  ...rest
}) {
  const norm = options.map(o => typeof o === 'string' ? {
    value: o,
    label: o
  } : o);
  const field = /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative',
      display: 'inline-flex',
      width: '100%'
    }
  }, /*#__PURE__*/React.createElement("select", _extends({
    id: id,
    value: value,
    defaultValue: defaultValue,
    onChange: onChange,
    disabled: disabled,
    style: {
      appearance: 'none',
      WebkitAppearance: 'none',
      width: '100%',
      padding: '10px 38px 10px 16px',
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-base)',
      fontWeight: 'var(--weight-medium)',
      color: 'var(--ink-900)',
      background: 'var(--surface-raised)',
      border: '1px solid var(--border-medium)',
      borderRadius: 'var(--radius-pill)',
      outline: 'none',
      cursor: 'pointer',
      boxShadow: 'var(--shadow-xs)',
      ...style
    },
    onFocus: e => {
      e.currentTarget.style.borderColor = 'var(--sage-500)';
      e.currentTarget.style.boxShadow = '0 0 0 3px rgba(126,147,141,0.25)';
    },
    onBlur: e => {
      e.currentTarget.style.borderColor = 'var(--border-medium)';
      e.currentTarget.style.boxShadow = 'var(--shadow-xs)';
    }
  }, rest), norm.map(o => /*#__PURE__*/React.createElement("option", {
    key: o.value,
    value: o.value
  }, o.label))), /*#__PURE__*/React.createElement("span", {
    "aria-hidden": "true",
    style: {
      position: 'absolute',
      right: '14px',
      top: '50%',
      transform: 'translateY(-50%)',
      pointerEvents: 'none',
      color: 'var(--ink-500)',
      fontSize: 'var(--text-sm)'
    }
  }, "\u25BE"));
  if (!label) return field;
  return /*#__PURE__*/React.createElement("label", {
    htmlFor: id,
    style: {
      display: 'block'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'block',
      marginBottom: '6px',
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-sm)',
      fontWeight: 'var(--weight-bold)',
      color: 'var(--ink-700)'
    }
  }, label), field);
}
Object.assign(__ds_scope, { Select });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Select.jsx", error: String((e && e.message) || e) }); }

// components/navigation/Navbar.jsx
try { (() => {
/**
 * Sakis Collection — Navbar
 * The app's top bar: a spinning vinyl logo, section links, and a
 * scoped search field. `logoSrc` should point at the vinyl-logo
 * asset relative to the host page.
 */
function Navbar({
  brand = 'Sakis Collection',
  logoSrc = 'assets/vinyl-logo.png',
  links = [],
  active = '',
  onNavigate,
  onSearch,
  spinning = true,
  style = {}
}) {
  return /*#__PURE__*/React.createElement("nav", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 'var(--space-5)',
      flexWrap: 'wrap',
      padding: 'var(--space-3) var(--space-5)',
      background: 'var(--surface-nav)',
      borderRadius: 'var(--radius-lg)',
      boxShadow: 'var(--shadow-sm)',
      ...style
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: '12px'
    }
  }, logoSrc && /*#__PURE__*/React.createElement("img", {
    src: logoSrc,
    alt: brand,
    width: 40,
    height: 40,
    style: {
      borderRadius: 'var(--radius-disc)',
      animation: spinning ? `sk-spin var(--spin-duration) linear infinite` : 'none'
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-display)',
      fontSize: 'var(--text-lg)',
      fontWeight: 'var(--weight-heavy)',
      color: 'var(--ink-900)',
      whiteSpace: 'nowrap'
    }
  }, brand)), /*#__PURE__*/React.createElement("ul", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: '2px',
      margin: 0,
      padding: 0,
      listStyle: 'none',
      flexWrap: 'wrap'
    }
  }, links.map(l => {
    const isActive = active === l.key;
    return /*#__PURE__*/React.createElement("li", {
      key: l.key
    }, /*#__PURE__*/React.createElement("button", {
      type: "button",
      onClick: () => onNavigate && onNavigate(l.key),
      style: {
        border: 'none',
        background: isActive ? 'var(--surface-raised)' : 'transparent',
        color: 'var(--ink-900)',
        fontFamily: 'var(--font-body)',
        fontSize: 'var(--text-base)',
        fontWeight: isActive ? 'var(--weight-bold)' : 'var(--weight-medium)',
        padding: '7px 14px',
        borderRadius: 'var(--radius-pill)',
        cursor: 'pointer',
        boxShadow: isActive ? 'var(--shadow-xs)' : 'none',
        transition: 'background var(--duration-fast) var(--ease-standard)'
      },
      onMouseEnter: e => {
        if (!isActive) e.currentTarget.style.background = 'var(--sage-100)';
      },
      onMouseLeave: e => {
        if (!isActive) e.currentTarget.style.background = 'transparent';
      }
    }, l.label));
  })), /*#__PURE__*/React.createElement("form", {
    role: "search",
    onSubmit: e => {
      e.preventDefault();
      onSearch && onSearch(e.currentTarget.q.value);
    },
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      marginLeft: 'auto'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative',
      display: 'flex',
      alignItems: 'center'
    }
  }, /*#__PURE__*/React.createElement("span", {
    "aria-hidden": "true",
    style: {
      position: 'absolute',
      left: '14px',
      color: 'var(--ink-500)',
      pointerEvents: 'none'
    }
  }, /*#__PURE__*/React.createElement("i", {
    className: "fa-solid fa-magnifying-glass"
  })), /*#__PURE__*/React.createElement("input", {
    name: "q",
    type: "search",
    placeholder: "\u0391\u03BD\u03B1\u03B6\u03AE\u03C4\u03B7\u03C3\u03B7\u2026",
    style: {
      padding: '8px 16px 8px 38px',
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-sm)',
      color: 'var(--ink-900)',
      background: 'var(--surface-raised)',
      border: '1px solid var(--border-medium)',
      borderRadius: 'var(--radius-pill)',
      outline: 'none',
      width: '180px'
    }
  }))), /*#__PURE__*/React.createElement("style", null, `@keyframes sk-spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`));
}
Object.assign(__ds_scope, { Navbar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/Navbar.jsx", error: String((e && e.message) || e) }); }

// components/navigation/Pagination.jsx
try { (() => {
/**
 * Sakis Collection — Pagination
 * Centered prev / page-numbers / next, matching the original app's
 * Bootstrap pagination, restyled as soft pills.
 */
function Pagination({
  page = 1,
  pages = 1,
  onChange,
  style = {}
}) {
  if (pages <= 1) return null;

  // Build a compact window of page numbers with ellipses.
  const items = [];
  const add = p => items.push(p);
  const window = 1;
  for (let p = 1; p <= pages; p++) {
    if (p === 1 || p === pages || p >= page - window && p <= page + window) {
      add(p);
    } else if (items[items.length - 1] !== '…') {
      add('…');
    }
  }
  const chip = (content, {
    active = false,
    disabled = false,
    onClick,
    key
  }) => /*#__PURE__*/React.createElement("button", {
    key: key,
    type: "button",
    disabled: disabled,
    "aria-current": active ? 'page' : undefined,
    onClick: onClick,
    style: {
      minWidth: '38px',
      height: '38px',
      padding: '0 10px',
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-base)',
      fontWeight: 'var(--weight-bold)',
      color: active ? 'var(--paper-50)' : disabled ? 'var(--ink-300)' : 'var(--ink-700)',
      background: active ? 'var(--rose-400)' : 'var(--surface-raised)',
      border: `1px solid ${active ? 'var(--rose-400)' : 'var(--border-medium)'}`,
      borderRadius: 'var(--radius-pill)',
      cursor: disabled || content === '…' ? 'default' : 'pointer',
      opacity: disabled ? 0.5 : 1,
      transition: 'all var(--duration-fast) var(--ease-standard)'
    }
  }, content);
  return /*#__PURE__*/React.createElement("nav", {
    "aria-label": "\u03A3\u03B5\u03BB\u03B9\u03B4\u03BF\u03C0\u03BF\u03AF\u03B7\u03C3\u03B7",
    style: {
      display: 'flex',
      justifyContent: 'center',
      gap: '6px',
      flexWrap: 'wrap',
      ...style
    }
  }, chip('‹ Προηγούμενη', {
    disabled: page <= 1,
    onClick: () => onChange && onChange(page - 1),
    key: 'prev'
  }), items.map((p, i) => p === '…' ? chip('…', {
    disabled: true,
    key: `e${i}`
  }) : chip(p, {
    active: p === page,
    onClick: () => onChange && onChange(p),
    key: p
  })), chip('Επόμενη ›', {
    disabled: page >= pages,
    onClick: () => onChange && onChange(page + 1),
    key: 'next'
  }));
}
Object.assign(__ds_scope, { Pagination });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/Pagination.jsx", error: String((e && e.message) || e) }); }

// ui_kits/sakis-collection/App.jsx
try { (() => {
/* Sakis Collection — UI kit app.
   Composes the design-system components into the redesigned
   catalogue, with the Greek-alphabet filter as the centrepiece.
   Exposes window.SakisApp. */
(function () {
  const NS = window.SakisCollectionDesignSystem_2efc19;
  const {
    Navbar,
    GreekAlphabetFilter,
    SongCard,
    DiskCard,
    Select,
    Pagination,
    Button,
    Badge,
    Input
  } = NS;

  /* Normalise a string's first character to a base Greek capital
     letter (strip tonos/dialytika, fold final sigma). */
  function firstLetter(str) {
    if (!str) return '#';
    const ch = str.trim().charAt(0).toUpperCase();
    const base = ch.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    const folded = base === 'Σ' ? 'Σ' : base;
    return /[Α-Ω]/.test(folded) ? folded : '#';
  }
  const NAV_LINKS = [{
    key: 'songs',
    label: 'Τραγούδια'
  }, {
    key: 'disks',
    label: 'Δίσκοι'
  }, {
    key: 'persons',
    label: 'Πρόσωπα'
  }, {
    key: 'companies',
    label: 'Εταιρείες'
  }, {
    key: 'labels',
    label: 'Ετικέτες'
  }];
  const SORTS = [{
    value: 'az',
    label: 'Τίτλος Α→Ω'
  }, {
    value: 'za',
    label: 'Τίτλος Ω→Α'
  }];
  const PER_PAGE = ['6', '8', '12'];
  function HeroHeader({
    section
  }) {
    const titles = {
      songs: 'Τραγούδια',
      disks: 'Δίσκοι',
      persons: 'Πρόσωπα',
      companies: 'Εταιρείες',
      labels: 'Ετικέτες'
    };
    const subtitle = section === 'songs' ? 'Όλα τα τραγούδια της συλλογής — φιλτράρισμα κατά αρχικό γράμμα' : section === 'disks' ? 'Όλοι οι δίσκοι βινυλίου — φιλτράρισμα κατά αρχικό γράμμα' : 'Η συλλογή του Σάκη';
    return React.createElement('div', {
      style: {
        display: 'flex',
        alignItems: 'center',
        gap: 'var(--space-5)',
        marginBottom: 'var(--space-6)'
      }
    }, React.createElement('img', {
      src: '../../assets/vinyl-logo.png',
      alt: '',
      width: 76,
      height: 76,
      style: {
        borderRadius: 'var(--radius-disc)',
        boxShadow: 'var(--shadow-disc)',
        animation: 'sk-spin var(--spin-duration) linear infinite',
        flex: 'none'
      }
    }), React.createElement('div', null, React.createElement('h1', {
      style: {
        margin: 0,
        fontFamily: 'var(--font-display)',
        fontWeight: 900,
        fontSize: 'var(--text-3xl)',
        color: 'var(--ink-900)',
        lineHeight: 1.05
      }
    }, titles[section]), React.createElement('p', {
      style: {
        margin: '4px 0 0',
        fontFamily: 'var(--font-body)',
        fontSize: 'var(--text-md)',
        color: 'var(--ink-500)'
      }
    }, subtitle)));
  }
  function EmptyState({
    label
  }) {
    return React.createElement('div', {
      style: {
        textAlign: 'center',
        padding: 'var(--space-8) var(--space-4)',
        color: 'var(--ink-500)',
        fontFamily: 'var(--font-body)',
        fontSize: 'var(--text-md)'
      }
    }, label);
  }
  function DetailModal({
    item,
    kind,
    onClose
  }) {
    if (!item) return null;
    return React.createElement('div', {
      onClick: onClose,
      style: {
        position: 'fixed',
        inset: 0,
        background: 'rgba(31,41,55,0.45)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '24px',
        zIndex: 50
      }
    }, React.createElement('div', {
      onClick: e => e.stopPropagation(),
      style: {
        background: 'var(--surface-raised)',
        borderRadius: 'var(--radius-lg)',
        boxShadow: 'var(--shadow-lg)',
        maxWidth: 480,
        width: '100%',
        padding: 'var(--space-6)'
      }
    }, React.createElement('div', {
      style: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        gap: 12
      }
    }, React.createElement('h2', {
      style: {
        margin: 0,
        fontFamily: 'var(--font-display)',
        fontWeight: 800,
        fontSize: 'var(--text-2xl)',
        color: 'var(--rose-500)'
      }
    }, item.title || item.name), React.createElement(Button, {
      variant: 'ghost',
      size: 'sm',
      onClick: onClose
    }, '✕')), kind === 'song' ? React.createElement('div', {
      style: {
        marginTop: 12
      }
    }, React.createElement('p', {
      style: {
        margin: '0 0 6px',
        fontSize: 'var(--text-xs)',
        fontWeight: 700,
        letterSpacing: 'var(--tracking-caps)',
        textTransform: 'uppercase',
        color: 'var(--ink-500)'
      }
    }, 'Συντελεστές'), React.createElement('ul', {
      style: {
        margin: 0,
        paddingLeft: 18,
        color: 'var(--ink-700)',
        fontFamily: 'var(--font-body)'
      }
    }, item.contributors.map((c, i) => React.createElement('li', {
      key: i
    }, React.createElement('strong', null, c.name), c.roles && c.roles.length ? ' · ' + c.roles.join(', ') : ''))), item.notes ? React.createElement('p', {
      style: {
        marginTop: 12,
        color: 'var(--ink-500)'
      }
    }, item.notes) : null) : React.createElement('div', {
      style: {
        marginTop: 12,
        fontFamily: 'var(--font-body)',
        color: 'var(--ink-700)'
      }
    }, React.createElement('p', {
      style: {
        margin: '0 0 6px'
      }
    }, (item.company || 'Χωρίς εταιρεία') + (item.size ? ' · ' + item.size + '″' : '')), React.createElement('p', {
      style: {
        margin: '0 0 6px',
        fontFamily: 'var(--font-mono)',
        fontSize: 'var(--text-sm)',
        color: 'var(--ink-500)'
      }
    }, 'ID: ' + item.sakisid), React.createElement('div', {
      style: {
        marginTop: 8,
        display: 'flex',
        alignItems: 'center',
        gap: 8
      }
    }, React.createElement(Badge, {
      variant: 'count'
    }, item.songCount), ' τραγούδια'), item.notes ? React.createElement('p', {
      style: {
        marginTop: 12,
        color: 'var(--ink-500)'
      }
    }, item.notes) : null)));
  }
  function CatalogueView({
    section
  }) {
    const data = window.SAKIS_DATA;
    const isSongs = section === 'songs';
    const all = isSongs ? data.songs : data.disks;
    const keyOf = x => isSongs ? x.title : x.name;
    const [letter, setLetter] = React.useState('Όλα');
    const [sort, setSort] = React.useState('az');
    const [perPage, setPerPage] = React.useState('6');
    const [page, setPage] = React.useState(1);
    const [query, setQuery] = React.useState('');
    const [detail, setDetail] = React.useState(null);
    const available = React.useMemo(() => {
      const s = new Set();
      all.forEach(x => s.add(firstLetter(keyOf(x))));
      return s;
    }, [all]);
    const filtered = React.useMemo(() => {
      let list = all.slice();
      if (letter !== 'Όλα') list = list.filter(x => firstLetter(keyOf(x)) === letter);
      if (query.trim()) {
        const q = query.trim().toLowerCase();
        list = list.filter(x => keyOf(x).toLowerCase().includes(q));
      }
      list.sort((a, b) => keyOf(a).localeCompare(keyOf(b), 'el'));
      if (sort === 'za') list.reverse();
      return list;
    }, [all, letter, query, sort]);
    React.useEffect(() => {
      setPage(1);
    }, [letter, query, sort, perPage, section]);
    const pp = parseInt(perPage, 10);
    const pages = Math.max(1, Math.ceil(filtered.length / pp));
    const pageItems = filtered.slice((page - 1) * pp, page * pp);
    return React.createElement('div', null, React.createElement(HeroHeader, {
      section
    }), /* Greek alphabet filter — the centrepiece */
    React.createElement('div', {
      style: {
        background: 'var(--surface-raised)',
        border: '1px solid var(--border-soft)',
        borderRadius: 'var(--radius-lg)',
        boxShadow: 'var(--shadow-sm)',
        padding: 'var(--space-5)',
        marginBottom: 'var(--space-5)'
      }
    }, React.createElement('div', {
      style: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 'var(--space-3)',
        flexWrap: 'wrap',
        gap: 8
      }
    }, React.createElement('span', {
      style: {
        fontFamily: 'var(--font-body)',
        fontSize: 'var(--text-xs)',
        fontWeight: 700,
        letterSpacing: 'var(--tracking-caps)',
        textTransform: 'uppercase',
        color: 'var(--ink-500)'
      }
    }, 'Αλφαβητικό φίλτρο'), letter !== 'Όλα' ? React.createElement(Button, {
      variant: 'ghost',
      size: 'sm',
      onClick: () => setLetter('Όλα')
    }, '✕ Καθαρισμός') : null), React.createElement(GreekAlphabetFilter, {
      active: letter,
      onSelect: setLetter,
      available: available,
      size: 'md'
    })), /* Controls */
    React.createElement('div', {
      style: {
        display: 'flex',
        alignItems: 'flex-end',
        gap: 'var(--space-3)',
        flexWrap: 'wrap',
        marginBottom: 'var(--space-4)'
      }
    }, React.createElement('div', {
      style: {
        flex: '1 1 240px',
        minWidth: 200
      }
    }, React.createElement(Input, {
      icon: React.createElement('i', {
        className: 'fa-solid fa-magnifying-glass'
      }),
      placeholder: isSongs ? 'Αναζήτηση τραγουδιού…' : 'Αναζήτηση δίσκου…',
      value: query,
      onChange: e => setQuery(e.target.value)
    })), React.createElement('div', {
      style: {
        width: 170
      }
    }, React.createElement(Select, {
      label: 'Ταξινόμηση',
      options: SORTS,
      value: sort,
      onChange: e => setSort(e.target.value)
    })), React.createElement('div', {
      style: {
        width: 110
      }
    }, React.createElement(Select, {
      label: 'Ανά σελίδα',
      options: PER_PAGE,
      value: perPage,
      onChange: e => setPerPage(e.target.value)
    }))), React.createElement('p', {
      style: {
        textAlign: 'center',
        color: 'var(--ink-500)',
        fontFamily: 'var(--font-body)',
        fontSize: 'var(--text-sm)',
        margin: '0 0 var(--space-4)'
      }
    }, filtered.length === 0 ? '' : 'Εμφάνιση ' + pageItems.length + ' από ' + filtered.length + (isSongs ? ' τραγούδια' : ' δίσκους')), pageItems.length === 0 ? React.createElement(EmptyState, {
      label: 'Δεν βρέθηκαν αποτελέσματα για αυτό το γράμμα.'
    }) : React.createElement('div', {
      style: {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
        gap: 'var(--space-4)',
        marginBottom: 'var(--space-6)'
      }
    }, pageItems.map(x => isSongs ? React.createElement(SongCard, {
      key: x.id,
      title: x.title,
      contributors: x.contributors,
      notes: x.notes,
      onView: () => setDetail(x),
      onEdit: () => {},
      onDelete: () => {}
    }) : React.createElement(DiskCard, {
      key: x.id,
      name: x.name,
      company: x.company,
      size: x.size,
      sakisid: x.sakisid,
      songCount: x.songCount,
      notes: x.notes,
      onView: () => setDetail(x),
      onEdit: () => {},
      onDelete: () => {}
    }))), React.createElement(Pagination, {
      page,
      pages,
      onChange: setPage
    }), React.createElement(DetailModal, {
      item: detail,
      kind: isSongs ? 'song' : 'disk',
      onClose: () => setDetail(null)
    }));
  }
  function PlaceholderView({
    section
  }) {
    const labels = {
      persons: 'Πρόσωπα',
      companies: 'Εταιρείες',
      labels: 'Ετικέτες'
    };
    return React.createElement('div', null, React.createElement(HeroHeader, {
      section
    }), React.createElement('div', {
      style: {
        background: 'var(--surface-raised)',
        border: '1px dashed var(--border-medium)',
        borderRadius: 'var(--radius-lg)',
        padding: 'var(--space-8)',
        textAlign: 'center',
        color: 'var(--ink-500)',
        fontFamily: 'var(--font-body)'
      }
    }, 'Η ενότητα «' + labels[section] + '» χρησιμοποιεί το ίδιο αλφαβητικό φίλτρο και τις ίδιες κάρτες. (Δείγμα UI kit)'));
  }
  function App() {
    const [section, setSection] = React.useState('songs');
    return React.createElement('div', {
      style: {
        maxWidth: 'var(--container-lg)',
        margin: '0 auto',
        padding: 'var(--space-5)'
      }
    }, React.createElement(Navbar, {
      logoSrc: '../../assets/vinyl-logo.png',
      active: section,
      links: NAV_LINKS,
      onNavigate: setSection,
      style: {
        marginBottom: 'var(--space-7)'
      }
    }), section === 'songs' || section === 'disks' ? React.createElement(CatalogueView, {
      key: section,
      section
    }) : React.createElement(PlaceholderView, {
      section
    }));
  }
  window.SakisApp = App;
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/sakis-collection/App.jsx", error: String((e && e.message) || e) }); }

// ui_kits/sakis-collection/data.js
try { (() => {
/* Sample catalogue data for the Sakis Collection UI kit.
   Titles/artists are real rebetiko & laiko references used as
   factual catalogue entries. window.SAKIS_DATA. */
(function () {
  const songs = [{
    id: 1,
    title: 'Άνοιξε πέτρα',
    contributors: [{
      name: 'Βασίλης Τσιτσάνης',
      roles: ['Σύνθεση', 'Στίχοι']
    }, {
      name: 'Σωτηρία Μπέλλου',
      roles: ['Ερμηνεία']
    }],
    notes: 'Λαϊκό · δεκαετία ’50'
  }, {
    id: 2,
    title: 'Βαλεντίνα',
    contributors: [{
      name: 'Γιάννης Σπανός',
      roles: ['Σύνθεση']
    }],
    notes: 'Έντεχνο'
  }, {
    id: 3,
    title: 'Γαρύφαλλο στ’ αυτί',
    contributors: [{
      name: 'Μάνος Χατζιδάκις',
      roles: ['Σύνθεση']
    }, {
      name: 'Νίκος Γκάτσος',
      roles: ['Στίχοι']
    }],
    notes: ''
  }, {
    id: 4,
    title: 'Δυο πόρτες έχει η ζωή',
    contributors: [{
      name: 'Χρήστος Κολοκοτρώνης',
      roles: ['Στίχοι']
    }, {
      name: 'Στέλιος Καζαντζίδης',
      roles: ['Ερμηνεία']
    }],
    notes: 'Λαϊκό'
  }, {
    id: 5,
    title: 'Ένα όμορφο αμάξι',
    contributors: [{
      name: 'Μάρκος Βαμβακάρης',
      roles: ['Σύνθεση', 'Στίχοι', 'Ερμηνεία']
    }],
    notes: 'Ρεμπέτικο'
  }, {
    id: 6,
    title: 'Ζητάτε να σας πω',
    contributors: [{
      name: 'Βασίλης Τσιτσάνης',
      roles: ['Σύνθεση']
    }],
    notes: ''
  }, {
    id: 7,
    title: 'Η Σμυρνιά',
    contributors: [{
      name: 'Παναγιώτης Τούντας',
      roles: ['Σύνθεση']
    }, {
      name: 'Μαρίκα Νίνου',
      roles: ['Ερμηνεία']
    }],
    notes: 'Σμυρναίικο'
  }, {
    id: 8,
    title: 'Θάλασσα πλατιά',
    contributors: [{
      name: 'Σταύρος Ξαρχάκος',
      roles: ['Σύνθεση']
    }],
    notes: 'Έντεχνο λαϊκό'
  }, {
    id: 9,
    title: 'Ίσως αύριο',
    contributors: [{
      name: 'Μίμης Πλέσσας',
      roles: ['Σύνθεση']
    }],
    notes: ''
  }, {
    id: 10,
    title: 'Καημός',
    contributors: [{
      name: 'Μίκης Θεοδωράκης',
      roles: ['Σύνθεση']
    }, {
      name: 'Γρηγόρης Μπιθικώτσης',
      roles: ['Ερμηνεία']
    }],
    notes: 'Από τον κύκλο Επιτάφιος'
  }, {
    id: 11,
    title: 'Λιλή η σκανταλιάρα',
    contributors: [{
      name: 'Παναγιώτης Τούντας',
      roles: ['Σύνθεση', 'Στίχοι']
    }],
    notes: 'Ρεμπέτικο · 1936'
  }, {
    id: 12,
    title: 'Μάνα μου Ελλάς',
    contributors: [{
      name: 'Σταύρος Ξαρχάκος',
      roles: ['Σύνθεση']
    }, {
      name: 'Νίκος Ξυλούρης',
      roles: ['Ερμηνεία']
    }],
    notes: 'Ρεμπέτικο (1983)'
  }, {
    id: 13,
    title: 'Νύχτωσε χωρίς φεγγάρι',
    contributors: [{
      name: 'Απόστολος Καλδάρας',
      roles: ['Σύνθεση', 'Στίχοι']
    }],
    notes: 'Λαϊκό · 1947'
  }, {
    id: 14,
    title: 'Ξημερώνει',
    contributors: [{
      name: 'Σταμάτης Κραουνάκης',
      roles: ['Σύνθεση']
    }],
    notes: ''
  }, {
    id: 15,
    title: 'Όλη νύχτα',
    contributors: [{
      name: 'Χάρις Αλεξίου',
      roles: ['Ερμηνεία']
    }],
    notes: ''
  }, {
    id: 16,
    title: 'Πέντε Έλληνες στον Άδη',
    contributors: [{
      name: 'Μάνος Χατζιδάκις',
      roles: ['Σύνθεση']
    }],
    notes: 'Έντεχνο'
  }, {
    id: 17,
    title: 'Ρόδι',
    contributors: [{
      name: 'Νίκος Μαμαγκάκης',
      roles: ['Σύνθεση']
    }],
    notes: ''
  }, {
    id: 18,
    title: 'Συννεφιασμένη Κυριακή',
    contributors: [{
      name: 'Βασίλης Τσιτσάνης',
      roles: ['Σύνθεση', 'Στίχοι']
    }, {
      name: 'Πρόδρομος Τσαουσάκης',
      roles: ['Ερμηνεία']
    }],
    notes: 'Λαϊκό · 1948'
  }, {
    id: 19,
    title: 'Της αμυγδαλιάς τα φύλλα',
    contributors: [{
      name: 'Γιώργος Ζαμπέτας',
      roles: ['Σύνθεση']
    }],
    notes: ''
  }, {
    id: 20,
    title: 'Υπάρχω',
    contributors: [{
      name: 'Στέλιος Καζαντζίδης',
      roles: ['Ερμηνεία']
    }],
    notes: 'Λαϊκό'
  }, {
    id: 21,
    title: 'Φραγκοσυριανή',
    contributors: [{
      name: 'Μάρκος Βαμβακάρης',
      roles: ['Σύνθεση', 'Στίχοι', 'Ερμηνεία']
    }],
    notes: 'Ρεμπέτικο · 1935'
  }, {
    id: 22,
    title: 'Χάρτινο το φεγγαράκι',
    contributors: [{
      name: 'Μάνος Χατζιδάκις',
      roles: ['Σύνθεση']
    }, {
      name: 'Νίκος Γκάτσος',
      roles: ['Στίχοι']
    }],
    notes: ''
  }, {
    id: 23,
    title: 'Ψεύτικα τα λόγια τα μεγάλα',
    contributors: [{
      name: 'Σταύρος Ξαρχάκος',
      roles: ['Σύνθεση']
    }, {
      name: 'Νίκος Ξυλούρης',
      roles: ['Ερμηνεία']
    }],
    notes: ''
  }, {
    id: 24,
    title: 'Ωραία που είναι η νύχτα',
    contributors: [{
      name: 'Απόστολος Καλδάρας',
      roles: ['Σύνθεση']
    }],
    notes: ''
  }, {
    id: 25,
    title: 'Αχ Ελλάδα σ’ αγαπώ',
    contributors: [{
      name: 'Διονύσης Σαββόπουλος',
      roles: ['Σύνθεση', 'Στίχοι', 'Ερμηνεία']
    }],
    notes: ''
  }, {
    id: 26,
    title: 'Μπάλλος',
    contributors: [{
      name: 'Διονύσης Σαββόπουλος',
      roles: ['Σύνθεση']
    }],
    notes: ''
  }, {
    id: 27,
    title: 'Πάμε μια βόλτα στο φεγγάρι',
    contributors: [{
      name: 'Σταύρος Ξαρχάκος',
      roles: ['Σύνθεση']
    }],
    notes: ''
  }, {
    id: 28,
    title: 'Τα παιδιά κάτω στον κάμπο',
    contributors: [{
      name: 'Μίκης Θεοδωράκης',
      roles: ['Σύνθεση']
    }],
    notes: ''
  }];
  const disks = [{
    id: 1,
    name: 'Αρχοντορεμπέτικα',
    company: 'Columbia',
    size: 12,
    sakisid: 'SK-0101',
    songCount: 12,
    notes: 'Συλλογή 1934–1940'
  }, {
    id: 2,
    name: 'Βυζαντινοί ύμνοι',
    company: 'Lyra',
    size: 12,
    sakisid: 'SK-0114',
    songCount: 9,
    notes: ''
  }, {
    id: 3,
    name: 'Γειτονιά μου',
    company: 'Minos',
    size: 7,
    sakisid: 'SK-0140',
    songCount: 2,
    notes: '45 RPM single'
  }, {
    id: 4,
    name: 'Δρόμοι παλιοί',
    company: 'His Master’s Voice',
    size: 10,
    sakisid: 'SK-0155',
    songCount: 8,
    notes: 'Σμυρναίικα'
  }, {
    id: 5,
    name: 'Επιτάφιος',
    company: 'Columbia',
    size: 12,
    sakisid: 'SK-0162',
    songCount: 8,
    notes: 'Θεοδωράκης / Ρίτσος'
  }, {
    id: 6,
    name: 'Ζεϊμπέκικα',
    company: 'Odeon',
    size: 12,
    sakisid: 'SK-0170',
    songCount: 10,
    notes: ''
  }, {
    id: 7,
    name: 'Η μεγάλη συλλογή',
    company: 'Minos',
    size: 12,
    sakisid: 'SK-0188',
    songCount: 14,
    notes: 'Διπλός δίσκος'
  }, {
    id: 8,
    name: 'Λαϊκές επιτυχίες',
    company: 'Philips',
    size: 12,
    sakisid: 'SK-0201',
    songCount: 12,
    notes: ''
  }, {
    id: 9,
    name: 'Μικρά Ασία',
    company: 'Lyra',
    size: 12,
    sakisid: 'SK-0219',
    songCount: 11,
    notes: 'Προσφυγικά τραγούδια'
  }, {
    id: 10,
    name: 'Νυχτολούλουδα',
    company: 'Columbia',
    size: 7,
    sakisid: 'SK-0230',
    songCount: 2,
    notes: ''
  }, {
    id: 11,
    name: 'Ρεμπέτικα της Σμύρνης',
    company: 'Odeon',
    size: 12,
    sakisid: 'SK-0244',
    songCount: 10,
    notes: ''
  }, {
    id: 12,
    name: 'Συννεφιασμένη Κυριακή',
    company: 'HMV',
    size: 10,
    sakisid: 'SK-0251',
    songCount: 6,
    notes: ''
  }, {
    id: 13,
    name: 'Της ξενιτιάς',
    company: 'Minos',
    size: 12,
    sakisid: 'SK-0268',
    songCount: 12,
    notes: 'Καζαντζίδης'
  }, {
    id: 14,
    name: 'Φωνές της Αθήνας',
    company: 'Philips',
    size: 12,
    sakisid: 'SK-0277',
    songCount: 13,
    notes: ''
  }, {
    id: 15,
    name: 'Χορός του Ζαλόγγου',
    company: 'Lyra',
    size: 7,
    sakisid: 'SK-0290',
    songCount: 2,
    notes: '45 RPM single'
  }, {
    id: 16,
    name: 'Ωδές',
    company: 'Columbia',
    size: 12,
    sakisid: 'SK-0301',
    songCount: 9,
    notes: ''
  }];
  window.SAKIS_DATA = {
    songs,
    disks
  };
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/sakis-collection/data.js", error: String((e && e.message) || e) }); }

__ds_ns.DiskCard = __ds_scope.DiskCard;

__ds_ns.GREEK_LETTERS = __ds_scope.GREEK_LETTERS;

__ds_ns.GreekAlphabetFilter = __ds_scope.GreekAlphabetFilter;

__ds_ns.SongCard = __ds_scope.SongCard;

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.Input = __ds_scope.Input;

__ds_ns.Select = __ds_scope.Select;

__ds_ns.Navbar = __ds_scope.Navbar;

__ds_ns.Pagination = __ds_scope.Pagination;

})();
