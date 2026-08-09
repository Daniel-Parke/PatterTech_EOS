import { useState } from "react";
import type { FormEvent } from "react";
import { t } from "./i18n";

type Props = {
  basketCount: number;
};

const MIN_PASSWORD = 8;

export function SignupForm({ basketCount }: Props) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [failed, setFailed] = useState(false);

  function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (password.length < MIN_PASSWORD) {
      setFailed(true);
      setPassword("");
      return;
    }
    setFailed(false);
    window.location.assign("/welcome");
  }

  return (
    <main className="signup">
      {failed && (
        <div className="banner" role="alert">
          {t("signup.invalid")}
        </div>
      )}
      <h1 className="signup-title">{t("signup.title")}</h1>
      <p className="signup-intro">{t("signup.intro")}</p>
      <p className="basket-note">
        {t("basket.youHave") +
          " " +
          basketCount +
          " " +
          (basketCount === 1 ? t("basket.item") : t("basket.items")) +
          " " +
          t("basket.waiting")}
      </p>
      <form className="signup-form" onSubmit={onSubmit}>
        <div className="field">
          <label htmlFor="email">{t("signup.emailLabel")}</label>
          <input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />
        </div>
        <div className="field">
          <label htmlFor="password">{t("signup.passwordLabel")}</label>
          <input
            id="password"
            name="password"
            type="password"
            autoComplete="new-password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </div>
        <button className="submit" type="submit">
          {t("signup.submit")}
        </button>
        {failed && (
          <button
            className="retry"
            type="button"
            onClick={() => setFailed(false)}
          >
            Try again
          </button>
        )}
      </form>
      <p className="signup-alt">
        {t("signup.haveAccount")}{" "}
        <a href="/sessions/new">{t("signup.logIn")}</a>
      </p>
      <p className="signup-terms">{t("signup.terms")}</p>
    </main>
  );
}
