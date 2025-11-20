import React, { useState, useEffect } from 'react';
import defaultPlaceholder from '../../assets/placeholder.webp';

/**
 * SmartImage
 * Props:
 * - publicSrc: string URL under /assets/ (optional)
 * - bundledSrc: imported asset (optional)
 * - placeholder: fallback URL/string (optional)
 * - alt, className, other <img> props
 *
 * Behavior:
 * - Default to bundledSrc if provided.
 * - On a full browser reload (navigation type 'reload'), attempt a single
 *   fetch of publicSrc (no-cache). If it exists, use it and store existence
 *   in sessionStorage keyed by publicSrc to avoid re-fetching during the session.
 * - Do not auto-retry during runtime/HMR.
 */

const SmartImage = ({ publicSrc, bundledSrc, placeholder, alt, ...imgProps }) => {
  // Use an explicit default bundled fallback so callers don't need to pass placeholder everywhere
  const bundled = bundledSrc || placeholder || defaultPlaceholder;
  const [src, setSrc] = useState(bundled || publicSrc || '');

  useEffect(() => {
    if (!publicSrc) return; // nothing to check

    try {
      const navEntries = (performance.getEntriesByType && performance.getEntriesByType('navigation')) || [];
      const navType = (navEntries[0] && navEntries[0].type) || (performance.navigation && performance.navigation.type === 1 ? 'reload' : 'navigate');

      const key = `smartimg:${publicSrc}`;
      const cached = sessionStorage.getItem(key);

      if (navType === 'reload') {
        fetch(publicSrc, { method: 'GET', cache: 'no-store' })
          .then(resp => {
            if (resp.ok) {
              sessionStorage.setItem(key, 'true');
              setSrc(publicSrc);
            } else {
              sessionStorage.setItem(key, 'false');
              setSrc(bundled || publicSrc ? (bundled) : '');
            }
          })
          .catch(() => {
            sessionStorage.setItem(key, 'false');
            setSrc(bundledSrc || placeholder || '');
          });
      } else if (cached === 'true') {
        setSrc(publicSrc);
      } else {
        setSrc(bundled || '');
      }
    } catch (e) {
      setSrc(bundled || '');
    }
  }, [publicSrc, bundledSrc, placeholder]);

  const handleError = e => {
    try {
      if (publicSrc) sessionStorage.setItem(`smartimg:${publicSrc}`, 'false');
    } catch (_) {}
    e.target.src = placeholder || bundled || defaultPlaceholder;
  };

  return <img src={src} alt={alt} onError={handleError} {...imgProps} />;
};

export default SmartImage;
