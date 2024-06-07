import { defineStore } from 'pinia';
import axios from 'axios';
export const useCartStore = defineStore({
  id: 'cart',
  state: () => ({
    sections: [],
    cart: {},
    filter: {
      sectionId: 'All',
      maxPrice: 'Infinity',
    },
    searchProduct: '',
    showCart: false,
  }),
  actions: {
    toggleCart() {
      this.showCart = !this.showCart;
    },
    async fetchSections() {
        const accessToken = localStorage.getItem('access_token');
        axios.get('/api/sections', {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                })
                .then((response) => {
                    this.sections = response.data;
                })
                .catch((error) => {
                    console.error('Failed to fetch sections:', error);
                });
    },
    filterProduct(product) {
      const sectionFilter = this.filter.sectionId === 'All' || product.section_id === this.filter.sectionId;
      const priceFilter = product.rate_per_unit <= this.filter.maxPrice;
      return sectionFilter && priceFilter;
    },
    isSearchedProduct(product) {
      const searchText = this.searchProduct.trim();
      if (searchText) {
        return product.name.toLowerCase().includes(searchText.toLowerCase());
      }
      return true;
    },
    hasMatchingProducts(section) {
      return section.products.some(
        (product) => this.filterProduct(product) && this.isSearchedProduct(product)
      );
    },
    addToCart(product) {
      if (product.quantity_available > 0) {
        if (!this.cart[product.id]) {
          this.cart[product.id] = {
            id: product.id,
            productName: product.name,
            price: product.rate_per_unit,
            quantity: 1,
            available: product.quantity_available - 1,
          };
        } else {
          this.cart[product.id].quantity += 1;
          this.cart[product.id].available -= 1;
        }
        product.quantity_available -= 1;
        this.updateAvailableQuantities();
      }
    },
    updateCart(cart) {
      this.cart = { ...cart };
      this.updateAvailableQuantities();
    },
    updateAvailableQuantities() {
      this.sections.forEach((section) => {
        section.products.forEach((product) => {
          if (this.cart[product.id]) {
            product.quantity_available = this.cart[product.id].available;
          }
        });
      });
    },
  },
});
