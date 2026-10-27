// Playground da TorreJWT: o HTML chama a mesma API JSON do Thunder Client.
// Tokens ficam no sessionStorage (some ao fechar a aba) — só para a aula.

const CHAVE_ACCESS = "torrejwt_access";
const CHAVE_REFRESH = "torrejwt_refresh";
const CHAVE_USUARIO = "torrejwt_usuario";

const saida = document.getElementById("saida");
const statusHttp = document.getElementById("status-http");
const formLogin = document.getElementById("form-login");
const sessao = document.getElementById("sessao");

function cortar(token) {
    if (!token) return "(nenhum)";
    return token.slice(0, 22) + "…";
}

function mostrarSessao() {
    const usuario = JSON.parse(sessionStorage.getItem(CHAVE_USUARIO) || "null");
    const access = sessionStorage.getItem(CHAVE_ACCESS);
    if (!usuario || !access) {
        sessao.classList.add("oculto");
        return;
    }
    sessao.classList.remove("oculto");
    sessao.querySelector(".sessao-nome").textContent =
        `Crachá ativo: ${usuario.nome} (${usuario.papel})`;
    sessao.querySelector(".sessao-tokens").textContent =
        `access ${cortar(access)}  ·  refresh ${cortar(sessionStorage.getItem(CHAVE_REFRESH))}`;
}

function pintar(status, corpo) {
    statusHttp.textContent = `HTTP ${status}`;
    saida.textContent = typeof corpo === "string"
        ? corpo
        : JSON.stringify(corpo, null, 2);
}

async function chamar(url, opcoes = {}) {
    const headers = { ...(opcoes.headers || {}) };
    const usarRefresh = opcoes.usarRefresh === true;
    const token = sessionStorage.getItem(usarRefresh ? CHAVE_REFRESH : CHAVE_ACCESS);
    if (token && opcoes.semAuth !== true) {
        headers.Authorization = `Bearer ${token}`;
    }
    if (opcoes.body && !headers["Content-Type"]) {
        headers["Content-Type"] = "application/json";
    }

    const resposta = await fetch(url, { method: opcoes.method || "GET", headers, body: opcoes.body });
    let corpo;
    try {
        corpo = await resposta.json();
    } catch {
        corpo = await resposta.text();
    }
    pintar(resposta.status, corpo);
    return { resposta, corpo };
}

function guardarTokens(corpo) {
    if (corpo.access_token) sessionStorage.setItem(CHAVE_ACCESS, corpo.access_token);
    if (corpo.refresh_token) sessionStorage.setItem(CHAVE_REFRESH, corpo.refresh_token);
    if (corpo.usuario) sessionStorage.setItem(CHAVE_USUARIO, JSON.stringify(corpo.usuario));
    mostrarSessao();
}

formLogin.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    const dados = Object.fromEntries(new FormData(formLogin).entries());
    const { corpo } = await chamar("/api/auth/login", {
        method: "POST",
        semAuth: true,
        body: JSON.stringify(dados),
    });
    if (corpo.access_token) guardarTokens(corpo);
});

document.querySelectorAll(".chip").forEach((botao) => {
    botao.addEventListener("click", () => {
        formLogin.username.value = botao.dataset.user;
        formLogin.senha.value = botao.dataset.pass;
    });
});

const acoes = {
    async eu() {
        await chamar("/api/auth/eu");
    },
    async saguao() {
        await chamar("/api/torre/saguao");
    },
    async radar() {
        await chamar("/api/torre/radar");
    },
    async admin() {
        await chamar("/api/torre/admin");
    },
    async refresh() {
        const { corpo } = await chamar("/api/auth/refresh", {
            method: "POST",
            usarRefresh: true,
        });
        if (corpo.access_token) guardarTokens(corpo);
    },
    async senha() {
        const senhaAtual = formLogin.senha.value;
        await chamar("/api/auth/senha", {
            method: "POST",
            body: JSON.stringify({
                senha_atual: senhaAtual,
                senha_nova: senhaAtual,
            }),
        });
    },
    async logout() {
        await chamar("/api/auth/logout", { method: "DELETE" });
        const refresh = sessionStorage.getItem(CHAVE_REFRESH);
        if (refresh) {
            await chamar("/api/auth/logout", { method: "DELETE", usarRefresh: true });
        }
        sessionStorage.removeItem(CHAVE_ACCESS);
        sessionStorage.removeItem(CHAVE_REFRESH);
        sessionStorage.removeItem(CHAVE_USUARIO);
        mostrarSessao();
    },
};

sessao.querySelectorAll("[data-acao]").forEach((botao) => {
    botao.addEventListener("click", () => acoes[botao.dataset.acao]());
});

document.getElementById("btn-saguao-livre").addEventListener("click", () => {
    chamar("/api/torre/saguao", { semAuth: true });
});

mostrarSessao();
