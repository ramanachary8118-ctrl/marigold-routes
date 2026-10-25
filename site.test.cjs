const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync('frontend/index.html', 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
new vm.Script(script);
const values = { adults: '2', children: '1', name: 'Sample Traveller', phone: '9876543210', email: 'sample@example.com' };
const errors = {};
let hotel = '900';
let addons = [];
let stored = null;
const context = vm.createContext({
  Intl, Date, Number, String, Math, JSON,
  sel: { value: 'p1' }, dateEl: { value: '2099-01-01', min: '' },
  val: name => values[name],
  F: {
    querySelector: selector => selector.includes('hotel') ? { value: hotel } : Object.values(errors).some(Boolean) ? { focus() {} } : null,
    querySelectorAll: () => addons,
  },
  clearErrs: () => { for (const key in errors) delete errors[key]; },
  setErr: (key, message) => { errors[key] = message; },
  iso: date => date.toISOString().slice(0,10),
  parseISO: value => new Date(value + 'T00:00:00'),
  localStorage: { getItem: () => stored, setItem: (_, value) => { stored = value; } },
  toast() {},
});
const run = code => vm.runInContext(code, context);
run(script.slice(script.indexOf('var INR='), script.indexOf('/* ---------- illustrations')));
run(script.slice(script.indexOf('var DEST='), script.indexOf('/* ---------- hero')));
run(script.slice(script.indexOf('function calc(){'), script.indexOf('function update(){')));
run(script.slice(script.indexOf('function validate(){'), script.indexOf('/* ---------- bookings storage')));
run(script.slice(script.indexOf('var KEY='), script.indexOf('var pending=')));
assert.equal(run('DEST.length'), 8);
assert.equal(run('PKG.length'), 8);
assert.ok(run('PKG.every(p => dest(p.dest) && p.plan.length === p.days && p.nights === p.days - 1)'));
assert.equal(run('calc().total'), (2 * 28500 + .7 * 28500 + 3 * 5 * 900) * 1.05);
addons = [{dataset: {price: '650', per: 'person'}, value: 'insurance', closest: () => ({querySelector: () => ({firstChild: {textContent: 'Insurance'}})})}];
assert.equal(run('calc().total'), (2 * 28500 + .7 * 28500 + 3 * 5 * 900 + 3 * 650) * 1.05);
assert.equal(run('validate()'), true);
values.adults = '1.5';
assert.equal(run('validate()'), false);
assert.ok(errors.ad);
values.adults = '2'; values.children = '';
assert.equal(run('validate()'), false);
values.children = '0'; context.dateEl.value = '2020-01-01';
assert.equal(run('validate()'), false);
assert.ok(errors.date);
stored = '[null, {"ref":"bad"}]';
assert.equal(run('load().length'), 0);
stored = '{broken';
assert.equal(run('load().length'), 0);
run('save([{ref: "MR-261026-ABCD", pkg: "Kerala", when: "1 Jan", hotel: "Standard", name: "Sample", ad: 2, ch: 0, total: 59850}])');
assert.equal(run('load().length'), 1);
assert.equal(run('load()[0].total'), 59850);
assert.ok(run('/^MR-[0-9]{6}-[A-Z2-9]{4}$/.test(ref())'));
assert.match(html, /<html lang="en">/);
assert.match(html, /no payment or real reservation is made/);
console.log('Passed: eight trip itineraries, pricing with children/upgrades/extras/tax, traveller and date validation, corrupt storage recovery, booking persistence, reference format, demo disclosure.');
