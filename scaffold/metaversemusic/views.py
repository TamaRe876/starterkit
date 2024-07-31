from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .models import Playlist, Charts, NFT
from .forms import PlaylistForm, NFTForm, CombinedForm
from web3 import Web3, HTTPProvider
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from blog.models import Post
from django.contrib import messages
from django.db import transaction
from web3.exceptions import Web3Exception
web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/e49caa765fe54cc2a3c6c49b241806e2"))
from .Web3 import calculate_minting_cost, send_transaction, get_transaction_receipt
from django.conf import settings

# Create a view to create a new NFT

class CreateNFTView(View):
    template_name = 'metaversemusic/create_nft.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = NFTForm()
        estimated_cost = calculate_minting_cost()
        context = {'form': form, 'estimated_cost': estimated_cost}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = CombinedForm(request.POST, request.FILES)
        if form.is_valid():
            nft_instance = form.cleaned_data['nft_form-nft']
            genre_instance = form.cleaned_data['genre_form-genre']

            nft_instance.owner = request.user

            try:
                user_profile = request.user.profile
                user_wallet_address = user_profile.bnb_wallet_address

                estimated_cost = calculate_minting_cost()
                
                transaction = {
                    "to": user_wallet_address,
                    "value": Web3.to_wei(estimated_cost, 'ether'),
                    "gas": 200000,  # You might want to estimate this dynamically as well
                    "gasPrice": Web3.to_wei('20', 'gwei'),  # You can adjust this or fetch dynamically
                }

                tx_hash = send_transaction(transaction, settings.PRIVATE_KEY)
                receipt = get_transaction_receipt(tx_hash)

                if receipt.status == 1:  # Transaction was successful
                    with transaction.atomic():
                        nft_instance.save()
                        nft_instance.genre.add(genre_instance)

                    messages.success(request, f"NFT created and minted successfully! Transaction hash: {tx_hash.hex()}")
                    return redirect('nft-detail', nft_id=nft_instance.pk)
                else:
                    messages.error(request, "Transaction failed. Please try again.")

            except Web3Exception as e:
                messages.error(request, f"Web3 error: {str(e)}")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")

        estimated_cost = calculate_minting_cost()
        context = {'form': form, 'estimated_cost': estimated_cost}
        return render(request, self.template_name, context)

# Create a view to list all the NFTs

def nftsmarket(request):
    nfts = NFT.objects.all()

    return render(request, 'metaversemusic/nftsmarket.html', {'nfts': nfts})


class MintingDetailsView(DetailView):
    template_name = 'metaversemusic/minting_details.html'

    def get(self, request, *args, **kwargs):
        nft_id = kwargs.get('nft_id')
        nft = get_object_or_404(NFT, id=nft_id)
        context = {'nft': nft}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        nft_id = kwargs.get('nft_id')
        nft = get_object_or_404(NFT, id=nft_id)

        minting_cost = request.POST.get('minting_cost')
        royalty_share = request.POST.get('royalty_share')

        nft.minting_cost = minting_cost
        nft.royalty_share = royalty_share
        nft.save()

        # Handle any additional logic or redirects

        context = {'nft': nft, 'success': True}
        return render(request, self.template_name, context)



class PlaylistListView(LoginRequiredMixin, ListView):
    model = Playlist
    template_name = 'metaversemusic/playlist_list.html'
    context_object_name = 'playlists'
    paginate_by = 10


class PlaylistDetailView(LoginRequiredMixin, DetailView):
    model = Playlist
    template_name = 'metaversemusic/playlist_detail.html'
    context_object_name = 'playlist'


class PlaylistCreateView(LoginRequiredMixin, CreateView):
    model = Playlist
    template_name = 'metaversemusic/playlist_create.html'
    form_class = PlaylistForm

    def form_valid(self, form):
        playlist = form.save(commit=False)
        playlist.user = self.request.user  # Set the user to the current authenticated user
        playlist.save()

        # Process the tags field
        tags_data = form.cleaned_data.get('tags')
        if tags_data:
            # Split the user-provided tags into a list
            tags_list = [tag.strip() for tag in tags_data.split(',') if tag.strip()]
            # Create Tag objects and add them to the playlist's tags
            for tag_name in tags_list:
                tag, created = tags_data.objects.get_or_create(name=tag_name)
                playlist.tags.add(tag)

        return redirect('playlist-list')  # Redirect to the playlist list view


class ChartsListView(ListView):
    model = Charts
    template_name = 'metaversemusic/chart_list.html'
    context_object_name = 'charts'
    paginate_by = 10


class ChartsDetailView(DetailView):
    model = Charts
    template_name = 'metaversemusic/chart_detail.html'
    context_object_name = 'chart'


