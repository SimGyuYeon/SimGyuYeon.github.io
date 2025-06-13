const endpoint = 'https://nameless-hat-e0af.sgy311.workers.dev';

function escapeHtml(str) {
  return str.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
}

function getTitle(item) {
  try {
    if (item.properties?.Title?.title?.length > 0) {
      return item.properties.Title.title[0].plain_text;
    }
    if (item.properties?.ingredient?.title?.length > 0) {
      return item.properties.ingredient.title[0].plain_text;
    }
  } catch (_) {}
  return '(제목 없음)';
}

async function loadData(type) {
  try {
    const res = await fetch(`${endpoint}/${type}`);
    const json = await res.json();
    const listEl = document.getElementById(`${type}-list`) || document.getElementById(`${type}s-list`);
    if (!listEl) return;
    listEl.innerHTML = '';

    json.results.forEach(item => {
      const title = escapeHtml(getTitle(item));
      const date = item.properties?.Date?.date?.start || item.properties?.expiration_date?.date?.start || '';
      const qty = item.properties?.Quantity?.number || '';
      const unit = item.properties?.Unit?.rich_text?.[0]?.text?.content || '';

      const row = document.createElement('tr');
      let html = '';

      if (type === 'meals') {
        html += `<td>${title}</td><td>${date}</td>`;
      } else if (type === 'fridge') {
        html += `<td>${title}</td><td>${qty}</td><td>${unit}</td>`;
      } else if (type === 'plans') {
        html += `<td>${title}</td><td>${date}</td>`;
      }

      html += `<td>
        <button onclick="editItem('${type}', '${item.id}', '${title}')">✏️</button>
        <button onclick="deleteItem('${type}', '${item.id}')">❌</button>
      </td>`;

      row.innerHTML = html;
      listEl.appendChild(row);
    });
  } catch (err) {
    console.error('데이터 로딩 오류:', err);
  }
}

async function addMeal() {
  const title = document.getElementById('meal-title').value;
  const date = document.getElementById('meal-date').value;
  await axios.post(`${endpoint}/meals`, { title, date });
  loadData('meals');
}

async function addFridge() {
  const name = document.getElementById('fridge-name').value;
  const quantity = Number(document.getElementById('fridge-qty').value);
  const unit = document.getElementById('fridge-unit').value;
  await axios.post(`${endpoint}/fridge`, { name, quantity, unit });
  loadData('fridge');
}

async function addPlan() {
  const title = document.getElementById('plan-title').value;
  const date = document.getElementById('plan-date').value;
  await axios.post(`${endpoint}/plans`, { title, date });
  loadData('plans');
}

async function editItem(type, id, oldTitle) {
  const newTitle = prompt('새 이름으로 수정:', oldTitle);
  if (!newTitle) return;
  await axios.patch(`${endpoint}/${type}/${id}`, { title: newTitle });
  loadData(type);
}

async function deleteItem(type, id) {
  if (!confirm('정말 삭제하시겠습니까?')) return;
  await axios.patch(`${endpoint}/${type}/${id}`, { archive: true });
  loadData(type);
}

window.onload = () => {
  loadData('meals');
  loadData('fridge');
  loadData('plans');
};
