export const DOCTOR_MESSAGES = Object.freeze({
  en: Object.freeze({
    caseLockBlocked:
      "This case is locked by an active or unverified owner. Keep the lock and original case. View its saved status without a new check, wait for the owning Doctor action to finish, or explicitly start a separate case. Do not delete the lock or stop a process to continue.",
    caseLockCleanupFailed:
      "The case action and lock cleanup have separate errors below. Preserve the original case and lock; inspect saved status before retrying.",
    connectionDisabled:
      "Keep the connection disabled. Reconnect only if the user explicitly asks.",
    desktopNativeRecheck:
      "Run a safe read from the target host. Local IPC checks do not prove that this conversation has recovered.",
    desktopReloadAndRecheck:
      "Reload the host connection in the same configuration scope, then make and record one native read-only tool call.",
    desktopRepairUnavailable:
      "The evidence does not support repairing a missing managed registration. Preserve the existing configuration, disabled setting and conflicts.",
    desktopSignIn:
      "Sign in normally in the selected ChatCut instance, then resume this case and recheck.",
    disabledRecheckRejected:
      "An intentionally disabled connection cannot be marked recovered from a successful recheck. Preserve the disabled setting.",
    hostedAuthenticateAndRecheck:
      "Complete any required sign-in or connection reload in the same host and configuration scope, then run native list_projects. Registration alone does not prove recovery.",
    hostedDisabled:
      "Keep the Hosted connection disabled; do not probe, repair or upload a report.",
    hostedNativeRecheck:
      "Run safe list_projects from the original host. Anonymous probes and configuration queries do not prove session recovery.",
    hostedRepairUnavailable:
      "Only a confirmed missing manual registration can be repaired. Do not change configuration after a failed lookup or for a plugin-managed service.",
    hostedTargetMismatch:
      "The native endpoint or scope differs from the selected target. No endpoint was changed and no probe was sent.",
    invalidNativeEvidence:
      "The recheck evidence was not accepted. Preserve the original report and obtain the target host's actual read-only result.",
    localProgramUnavailable:
      "Preserve the original error, check whether the selected local program or instance is available, and continue this case. Nothing was installed, no environment was switched, and no credentials were cleared.",
    nativeHostReadRequired:
      "Continue in the selected native host: run Desktop read_project with the actual projectId, or Hosted list_projects, and record its actual output for this case. A login or new session may be needed. Keep the same case; configuration checks cannot replace this read.",
    resultHealthy: "Current checks passed",
    resultNeedsUser: "Action needed",
    resultRecovered: "Recovered",
    resultUnresolved: "Unresolved",
  }),
  es: Object.freeze({
    caseLockBlocked:
      "Este caso está bloqueado por un proceso activo o cuyo estado no se puede confirmar. Conserva el bloqueo y el caso original. Consulta el estado guardado sin ejecutar otra comprobación, espera a que termine la acción de Doctor o inicia expresamente otro caso. No borres el bloqueo ni detengas un proceso para continuar.",
    caseLockCleanupFailed:
      "Los errores de la acción y de la liberación del bloqueo aparecen por separado a continuación. Conserva el caso original y el bloqueo; consulta el estado guardado antes de reintentar.",
    connectionDisabled:
      "Mantén la conexión desactivada. Vuelve a conectarla solo si el usuario lo pide expresamente.",
    desktopNativeRecheck:
      "Ejecuta una consulta segura desde el cliente de destino. Las comprobaciones de IPC local no demuestran que esta conversación haya recuperado la conexión.",
    desktopReloadAndRecheck:
      "Recarga la conexión del cliente en el mismo ámbito de configuración; después, ejecuta y registra una llamada nativa de solo lectura.",
    desktopRepairUnavailable:
      "Las pruebas no justifican reparar un registro administrado ausente. Conserva la configuración actual, la desactivación y los conflictos detectados.",
    desktopSignIn:
      "Inicia sesión con el procedimiento habitual en la instancia de ChatCut seleccionada; después, retoma este caso y vuelve a comprobar la conexión.",
    disabledRecheckRejected:
      "Una conexión desactivada deliberadamente no puede marcarse como restablecida por una comprobación exitosa. Mantén la desactivación.",
    hostedAuthenticateAndRecheck:
      "Completa el inicio de sesión o la recarga de conexión que hagan falta en el mismo cliente y ámbito de configuración; después, ejecuta list_projects de forma nativa. El registro por sí solo no demuestra que se haya restablecido la conexión.",
    hostedDisabled:
      "Mantén desactivada la conexión de Hosted; no ejecutes pruebas ni reparaciones y no envíes informes.",
    hostedNativeRecheck:
      "Ejecuta list_projects de forma segura desde el cliente original. Las pruebas anónimas y las consultas de configuración no demuestran que la sesión haya recuperado la conexión.",
    hostedRepairUnavailable:
      "Solo se puede reparar un registro manual cuya ausencia esté confirmada. No cambies la configuración si falla la consulta o si el servicio lo administra un plugin.",
    hostedTargetMismatch:
      "La dirección o el ámbito de la configuración nativa no coinciden con el destino seleccionado. No se ha cambiado la dirección ni enviado ninguna prueba.",
    invalidNativeEvidence:
      "No se han aceptado las pruebas de la comprobación. Conserva el informe original y obtén el resultado real de una consulta de solo lectura desde el cliente de destino.",
    localProgramUnavailable:
      "Conserva el error original, comprueba si el programa o la instancia local seleccionados están disponibles y continúa este caso. No se ha instalado nada, cambiado de entorno ni borrado credenciales.",
    nativeHostReadRequired:
      "Continúa en el cliente seleccionado: ejecuta read_project de Desktop con el projectId real, o list_projects de Hosted, y guarda el resultado real en este caso. Puede ser necesario iniciar sesión o abrir una nueva sesión. Conserva el mismo caso; comprobar la configuración no sustituye esta lectura.",
    resultHealthy: "Comprobaciones actuales correctas",
    resultNeedsUser: "Se necesita tu intervención",
    resultRecovered: "Conexión restablecida",
    resultUnresolved: "Sin resolver",
  }),
  zh: Object.freeze({
    caseLockBlocked:
      "此案例的锁仍由活跃或状态无法确认的进程持有。请保留锁和原案例，只读查看已保存状态，等待原 Doctor 操作结束，或明确另建案例。不要通过删锁或终止进程继续。",
    caseLockCleanupFailed:
      "案例操作与锁清理的错误在下方分别保留。请保留原案例和锁，先查看已保存状态再重试。",
    connectionDisabled: "保留主动禁用选择；仅在用户明确要求重新连接时处理。",
    desktopNativeRecheck:
      "由目标宿主实际执行安全读取；本地 IPC 检查不能证明当前对话已恢复。",
    desktopReloadAndRecheck:
      "在相同配置范围重载宿主连接，执行一次原生只读工具调用并记录。",
    desktopRepairUnavailable:
      "当前证据不满足缺失受管理注册的限定修复条件；配置、禁用选择和冲突保持原样。",
    desktopSignIn: "在所选 ChatCut 实例中完成正常登录，再继续同一事件复检。",
    disabledRecheckRejected:
      "主动禁用的连接不能凭复检成功标记为已恢复；请保留禁用选择。",
    hostedAuthenticateAndRecheck:
      "在同一宿主及配置范围完成需要的认证或连接重载，再执行原生 list_projects；注册成功不等于恢复。",
    hostedDisabled: "保留主动禁用的 Hosted 连接；不探测、不修复、不上传。",
    hostedNativeRecheck:
      "原宿主执行安全 list_projects；匿名探测或配置查询不能证明会话恢复。",
    hostedRepairUnavailable:
      "仅支持明确缺失的手动注册；查询失败或插件管理的服务不修改。",
    hostedTargetMismatch:
      "原生配置地址或作用域与所选目标不一致；未切换地址或发送探测。",
    invalidNativeEvidence:
      "实际复检证据未被接受；保留原报告并取得目标宿主的真实只读结果。",
    localProgramUnavailable:
      "保留原始错误；检查所选本地程序或实例是否可用，继续同一事件。没有安装、切换环境或清理凭据。",
    nativeHostReadRequired:
      "请在目标宿主调用 Desktop read_project（使用真实 projectId）或 Hosted list_projects，并将实际输出保存到同一事件。可能需要正常登录或新会话；配置检查不能代替这次读取。",
    resultHealthy: "当前检查正常",
    resultNeedsUser: "需要用户参与",
    resultRecovered: "已恢复",
    resultUnresolved: "尚未解决",
  }),
});

export function doctorLocale(env = process.env) {
  const locale =
    [env.LC_ALL, env.LC_MESSAGES, env.LANG]
      .find((value) => typeof value === "string" && value.trim())
      ?.trim()
      .toLowerCase() ?? "en";
  if (/^zh(?:[-_.@]|$)/u.test(locale)) return "zh";
  if (/^es(?:[-_.@]|$)/u.test(locale)) return "es";
  return "en";
}

export function doctorMessage(key, env = process.env) {
  if (!Object.hasOwn(DOCTOR_MESSAGES.en, key))
    throw new Error(`Unknown Doctor message: ${key}`);
  return DOCTOR_MESSAGES[doctorLocale(env)][key];
}
