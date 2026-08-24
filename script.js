const filters = document.querySelectorAll('.filter');
const resources = document.querySelectorAll('.resource-card');

filters.forEach((filter) => {
  filter.addEventListener('click', () => {
    const selected = filter.dataset.filter;
    filters.forEach((item) => item.classList.toggle('active', item === filter));
    resources.forEach((resource) => {
      resource.classList.toggle('hidden', selected !== 'all' && resource.dataset.type !== selected);
    });
  });
});

const menuButton = document.querySelector('.menu-button');
const navigation = document.querySelector('#navigation');

menuButton.addEventListener('click', () => {
  const isOpen = navigation.classList.toggle('open');
  menuButton.setAttribute('aria-expanded', String(isOpen));
});

navigation.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    navigation.classList.remove('open');
    menuButton.setAttribute('aria-expanded', 'false');
  });
});
