import { SignupForm } from "./SignupForm";
import { t } from "./i18n";

const basket = { count: 3 };

export function App() {
  return (
    <div className="page">
      <header className="site-header">
        <span className="brand">{t("nav.brand")}</span>
        <nav className="site-nav">
          <a className="nav-link" href="/basket">
            {t("nav.basket")}
          </a>
          <a className="nav-link" href="/sessions/new">
            {t("nav.signIn")}
          </a>
        </nav>
      </header>
      <SignupForm basketCount={basket.count} />
    </div>
  );
}
