//Users module handles the fetching of users as well as deleting the user, will integrate when required.
// CUrrently unused


import { userService } from '../_services';

const state = {
    all: {}
};

const actions = {
	getAll({ commit }) {
        commit('getAllRequest');

        userService.getAll()
            .then(
                users => commit('getAllSuccess', users),
                error => commit('getAllFailure', error)
            );
    },
};

const mutations = {
	getAllRequest(state) {
        state.all = { loading: true };
    },
    getAllSuccess(state, users) {
        state.all = { items: users };
    },
    getAllFailure(state, error) {
        state.all = { error };
    },
};

export const users = {
    namespaced: true,
    state,
    actions,
    mutations
};