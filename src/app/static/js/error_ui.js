// Lightweight Error UI utilities: toasts, modal errors, confirm, field validation, and fetch wrapper
// Usage examples:
//   ErrorUI.showToast('Message', {type:'error', actionLabel:'Retry', action: ()=>{...}})
//   const modal = ErrorUI.showModalError({title:'Server error', message:'Something went wrong'});
//   ErrorUI.wrapFetch('/api', {}, {retry:true}).then(r=>r.json())

(function(){
  const TOAST_TIMEOUT = 5000;

  function ensureContainer(){
    let c = document.getElementById('errorui_toasts');
    if(!c){
      c = document.createElement('div');
      c.id = 'errorui_toasts';
      c.style.position = 'fixed';
      c.style.zIndex = '9999';
      c.style.right = '12px';
      c.style.top = '12px';
      c.style.display = 'flex';
      c.style.flexDirection = 'column';
      c.style.gap = '8px';
      document.body.appendChild(c);
    }
    return c;
  }

  function showToast(message, opts){
    opts = opts || {};
    const type = opts.type || 'info';
    const actionLabel = opts.actionLabel;
    const action = opts.action;
    const dismissTimeout = typeof opts.dismissTimeout === 'number' ? opts.dismissTimeout : (type === 'error' ? 0 : TOAST_TIMEOUT);
    const container = ensureContainer();
    const el = document.createElement('div');
    el.className = 'eu-toast eu-toast-'+type;
    el.style.minWidth = '240px';
    el.style.padding = '8px 12px';
    el.style.borderRadius = '8px';
    el.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)';
    el.style.background = '#fff';
    el.style.border = '1px solid #ddd';
    const text = document.createElement('div');
    text.style.fontSize = '14px';
    text.style.color = '#222';
    text.textContent = message;
    if(actionLabel && typeof action === 'function'){
      const wrap = document.createElement('div');
      wrap.style.display = 'flex';
      wrap.style.justifyContent = 'space-between';
      wrap.style.alignItems = 'center';
      const btn = document.createElement('button');
      btn.textContent = actionLabel;
      btn.style.marginLeft = '8px';
      btn.style.padding = '6px 8px';
      btn.style.border = 'none';
      btn.style.background = '#007bff';
      btn.style.color = 'white';
      btn.style.borderRadius = '6px';
      btn.addEventListener('click', ()=>{ try{ action(); }catch(e){ console.warn(e); } finally { try{ el.remove(); }catch(_){} } });
      wrap.appendChild(text);
      wrap.appendChild(btn);
      el.appendChild(wrap);
    } else {
      el.appendChild(text);
    }
    container.appendChild(el);
    if(dismissTimeout>0) setTimeout(()=>{ try{ el.remove(); }catch(e){} }, dismissTimeout);
    return {el, dismiss: ()=>{ try{ el.remove(); }catch(e){} }};
  }

  function showModalError({title='Помилка', message='', why='', next='', estimatedRecovery=null} = {}){
    let modal = document.getElementById('errorui_modal');
    if(!modal){
      modal = document.createElement('div');
      modal.id = 'errorui_modal';
      modal.className = 'eu-modal-backdrop';
      modal.innerHTML = `
        <div class="eu-modal-card" role="dialog" aria-modal="true" aria-labelledby="eu_modal_title">
          <h2 id="eu_modal_title"></h2>
          <div id="eu_modal_message" class="eu-modal-message"></div>
          <div id="eu_modal_why" class="eu-modal-why muted"></div>
          <div id="eu_modal_next" class="eu-modal-next"></div>
          <div style="text-align:right;margin-top:12px">
            <button id="eu_modal_retry" class="btn">Retry</button>
            <button id="eu_modal_close" class="btn" style="margin-left:8px">Close</button>
          </div>
        </div>
      `;
      document.body.appendChild(modal);
      modal.querySelector('#eu_modal_close').addEventListener('click', ()=>{ modal.style.display='none'; });
      modal.querySelector('#eu_modal_retry').addEventListener('click', ()=>{ modal.style.display='none'; if(typeof modal._onRetry === 'function'){ modal._onRetry(); } });
    }
    modal.style.display = 'block';
    modal.querySelector('#eu_modal_title').textContent = title;
    modal.querySelector('#eu_modal_message').textContent = message;
    modal.querySelector('#eu_modal_why').textContent = why ? ('Чому: ' + why) : '';
    modal.querySelector('#eu_modal_next').textContent = next ? ('Що робити далі: ' + next) : '';
    if(estimatedRecovery) modal.querySelector('#eu_modal_next').textContent += (modal.querySelector('#eu_modal_next').textContent ? ' ' : '') + ('Очікуваний час відновлення: ' + estimatedRecovery);
    modal._onRetry = null;
    return {
      onRetry(fn){ if(typeof fn === 'function') modal._onRetry = fn; },
      close(){ modal.style.display = 'none'; }
    };
  }

  function showConfirm({title='Підтвердження', message='', confirmLabel='Підтвердити', cancelLabel='Відмінити'} = {}){
    return new Promise((resolve)=>{
      let existing = document.getElementById('errorui_confirm');
      if(!existing){
        const mod = document.createElement('div');
        mod.id = 'errorui_confirm';
        mod.className = 'eu-modal-backdrop';
        mod.innerHTML = `<div class="eu-modal-card"><h3 id="eu_confirm_title"></h3><div id="eu_confirm_message"></div><div style="text-align:right;margin-top:12px"><button id="eu_confirm_cancel" class="btn">${cancelLabel}</button><button id="eu_confirm_confirm" class="btn" style="margin-left:8px">${confirmLabel}</button></div></div>`;
        document.body.appendChild(mod);
        mod.querySelector('#eu_confirm_cancel').addEventListener('click', ()=>{ mod.style.display='none'; resolve(false); });
        mod.querySelector('#eu_confirm_confirm').addEventListener('click', ()=>{ mod.style.display='none'; resolve(true); });
        existing = mod;
      }
      existing.style.display = 'block';
      existing.querySelector('#eu_confirm_title').textContent = title;
      existing.querySelector('#eu_confirm_message').textContent = message;
    });
  }

  function attachFieldValidation(el, validator){
    if(!el || typeof validator !== 'function') return;
    let errorNode = el.nextElementSibling;
    if(!errorNode || !errorNode.classList.contains('eu-field-error')){
      errorNode = document.createElement('div');
      errorNode.className = 'eu-field-error';
      errorNode.style.color = '#a00';
      errorNode.style.marginTop = '6px';
      errorNode.style.fontSize = '13px';
      el.insertAdjacentElement('afterend', errorNode);
    }
    el.addEventListener('blur', function(){
      const val = el.value;
      let msg = null;
      try{ msg = validator(val); }catch(e){ msg = 'Невірне значення'; }
      if(msg){ el.classList.add('eu-field-invalid'); errorNode.textContent = msg; } else { el.classList.remove('eu-field-invalid'); errorNode.textContent = ''; }
    });
  }

  function wrapFetch(input, init, opts){
    opts = opts || {};
    const attempt = ()=> fetch(input, init).then(async res => {
      if(res.ok) return res;
      const status = res.status;
      if(status === 403){
        showToast('Доступ заборонено: недостатньо прав.', {type:'error', actionLabel:'Деталі', action: ()=>{ showModalError({title:'Доступ заборонено (403)', message:'У вас немає достатніх прав для цієї дії.', why:'Потрібні дозволи: editor або admin', next:'Зверніться до адміністратора або користувача з правами admin для надання доступу.'}); }});
        throw new Error('403');
      } else if(status >= 500){
        const modal = showModalError({title:'Системна помилка', message:'Схоже, сталася помилка на сервері.', why:'Ми фіксуємо проблему та працюємо над виправленням.', next:'Спробуйте ще раз через деякий час. Якщо проблема не зникне, повідомте адміністратора.', estimatedRecovery:'≈15 хвилин'});
        modal.onRetry(()=>{ attempt(); });
        throw new Error(String(status));
      } else {
        let text = 'Сталася помилка. Спробуйте ще раз.';
        try{ const j = await res.json(); if(j && j.detail) text = j.detail; }catch(e){}
        showToast(text, {type:'error'});
        throw new Error(String(status));
      }
    }).catch(err => {
      // network error
      showToast('Мережна помилка. Перевірте підключення.', {type:'error', actionLabel:'Retry', action: attempt});
      throw err;
    });
    return attempt();
  }

  window.ErrorUI = { showToast, showModalError, showConfirm, attachFieldValidation, wrapFetch };

  // minimal CSS injection when no external style provided
  if(!document.getElementById('errorui_styles')){
    const style = document.createElement('style'); style.id = 'errorui_styles';
    style.textContent = `
      .eu-modal-backdrop{ position:fixed; inset:0; background:rgba(0,0,0,0.45); display:flex; align-items:center; justify-content:center; z-index:10000 }
      .eu-modal-card{ background:white; padding:16px; border-radius:8px; max-width:720px; width:90%; box-shadow:0 6px 30px rgba(0,0,0,0.25) }
      .eu-toast{ font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial }
      .eu-field-invalid{ border-color:#e00 !important; box-shadow:0 0 0 3px rgba(255,0,0,0.06) }
      .eu-field-error{ color:#a00; font-size:13px }
    `;
    document.head.appendChild(style);
  }

})();
